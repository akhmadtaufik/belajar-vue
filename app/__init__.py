import threading
import time
from datetime import timedelta

import schedule
from flask import Flask

# import flask admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

# import custom model view
from app.admin.CustomModelView import AdminModelView, CustomModelView
from app.auth import authBp
from app.extensions import db, jwt, login_manager, migrate
from app.frontend import frontendBp

# import models
from app.models.tweet import Tweets
from app.models.tweet_count import TweetCount
from app.models.user import Users
from app.scheduler.count_tweet import total_tweet
from app.tweet import tweetBp
from app.user import userBp
from config import Config


def create_app(config_class=Config):
    # Konfigurasi APP
    app = Flask(__name__)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config.from_object(config_class)

    # inisiasi admin panel
    admin = Admin(
        app,
        name="Dashboard",
        template_mode="bootstrap4",
        index_view=AdminModelView("home"),
        url="/",
    )

    # Initilizae database & migration
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)

    schedule.every(10).seconds.do(total_tweet)

    def run_schedule():
        with app.app_context():  # Ensure the app context is pushed
            while True:
                schedule.run_pending()
                time.sleep(2)

    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.daemon = True
    schedule_thread.start()

    admin.add_view(CustomModelView(Users, db.session))
    admin.add_view(CustomModelView(Tweets, db.session))
    admin.add_view(CustomModelView(TweetCount, db.session))

    # initilize blueprint
    app.register_blueprint(frontendBp, url_prefix="/")
    app.register_blueprint(tweetBp, url_prefix="/api/tweets")
    app.register_blueprint(userBp, url_prefix="/api/users")
    app.register_blueprint(authBp, url_prefix="/api/auth")

    return app
