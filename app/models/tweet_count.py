from app.extensions import db


class TweetCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    total_tweet = db.Column(db.Integer, default=0)

    def serialize(self):
        return {
            "id": self.id,
            "usernam": self.username,
            "total_tweet": self.total_tweet,
        }
