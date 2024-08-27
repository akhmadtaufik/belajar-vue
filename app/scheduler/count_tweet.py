from app.extensions import db
from app.models.tweet import Tweets
from app.models.tweet_count import TweetCount
from app.models.user import Users


def total_tweet():
    users = Users.query.all()
    user_post = {}

    for user in users:
        total_tweet = Tweets.query.filter(Tweets.user_id == user.user_id).count()
        user_post[user.username] = total_tweet

    sorted_post = sorted(user_post.items(), key=lambda x: x[1], reverse=True)

    existing_post_user = TweetCount.query.all()
    existing_user = {post_user.username: post_user for post_user in existing_post_user}

    for username, total_tweet in sorted_post:
        if username in existing_user:
            post_tweet_data = existing_user[username]
            post_tweet_data.total_tweet = total_tweet
        else:
            post_user = TweetCount(username=username, total_tweet=total_tweet)
            db.session.add(post_user)

        db.session.commit()
