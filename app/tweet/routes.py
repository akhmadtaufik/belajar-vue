import logging
import os
from datetime import datetime, timedelta

from flask import (
    jsonify,
    make_response,
    request,
    send_file,
    send_from_directory,
)
from flask_jwt_extended import get_jwt_identity, jwt_required
from minio import Minio
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.tweet import Tweets
from app.models.user import Users
from app.tweet import tweetBp

UPLOAD_FILE_LOCATION = "./static/uploaded/"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

BUCKET_NAME = "imagebucket"


client = Minio(
    "127.0.0.1:9000",
    access_key="nulltribe",
    secret_key="Rnpl1105",
    secure=False,
)
try:
    buckets = client.list_buckets()
    print("Connected to MinIO successfully")
except Exception as e:
    print(f"Failed to connect to MinIO: {e}")


def allowed_file(filename):
    """
    Cek apakah format file yang diupload benar
    """
    filename = filename.lower()
    extension = filename.split(".")[-1]

    return extension in ALLOWED_EXTENSIONS


@tweetBp.route("", methods=["GET"], strict_slashes=False)
@jwt_required(locations=["headers"], optional=True)
def get_tweet():
    limit = request.args.get("limit", 20)
    if type(limit) is not int:
        return jsonify({"message": "invalid parameter"}), 400

    user_id = get_jwt_identity()

    if not user_id:
        user_id = "None"
    else:
        user_id = user_id

    # get tweets by id
    tweets = db.session.execute(db.select(Tweets).limit(limit)).scalars()

    results = []
    for tweet in tweets:
        results.append(tweet.serialize())

    response = make_response(jsonify(user_id=user_id, data=results), 200)
    # response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@tweetBp.route("", methods=["POST"], strict_slashes=False)
@jwt_required(locations=["headers"])
def post_tweet():
    found = client.bucket_exists(BUCKET_NAME)
    if not found:
        client.make_bucket(BUCKET_NAME)
        print(f"Bucket '{BUCKET_NAME}' created successfully.")
    else:
        print(f"Bucket '{BUCKET_NAME}' already exists")
        try:
            client.list_buckets()
            print("Connected to MinIO successfully")
        except Exception as e:
            print(f"Failed to connect to MinIO: {e}")

    logging.info(f"Received request: {request}")
    logging.info(f"Request headers: {request.headers}")
    logging.info(f"Request form: {request.form}")
    logging.info(f"Request files: {request.files}")

    try:
        user_id = get_jwt_identity()
        logging.info(f"User ID from JWT: {user_id}")
    except Exception as e:
        logging.error(f"Error getting JWT identity: {e}")
        return jsonify({"error": "Invalid or missing JWT token"}), 401

    content_type = request.content_type or ""
    logging.info(f"Content-Type: {content_type}")

    if content_type.startswith("multipart/form-data"):
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files["file"]
        content = request.form.get("content")

        logging.info(f"File: {file}")
        logging.info(f"Content: {content}")

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        if not content or content.strip() == "":
            return jsonify({"error": "Tweet content cannot be empty"}), 400
        if file and allowed_file(file.filename):
            image_size = os.fstat(file.fileno()).st_size
            image_name = secure_filename(file.filename)
            client.put_object(BUCKET_NAME, image_name, file, image_size)
            image_path = client.presigned_get_object(
                BUCKET_NAME, image_name, expires=timedelta(days=7)
            )
            new_content = Tweets(
                content=content,
                user_id=user_id,
                image_name=image_name,
                image_path=image_path,
            )
            db.session.add(new_content)
            db.session.commit()
            return jsonify(data=new_content.serialize()), 200
    elif content_type.startswith("application/json"):
        data = request.get_json()
        if not data or "content" not in data:
            return jsonify({"error": "Invalid JSON data"}), 400
        content = data["content"]
    else:
        return (
            jsonify({"error": f"Unsupported media type: {content_type}"}),
            415,
        )

    if not content or content.strip() == "":
        return jsonify({"error": "Tweet content cannot be empty"}), 400

    try:
        tweet = Tweets(user_id=user_id, content=content)
        db.session.add(tweet)
        db.session.commit()
        return jsonify(data=tweet.serialize()), 200
    except Exception as e:
        logging.error(f"Error saving tweet to database: {e}")
        db.session.rollback()
        return jsonify({"error": f"Failed to save tweet: {str(e)}"}), 500


def serve_image(filename):
    """
    Serve uploaded image
    """

    img_directory = "./static/uploaded"
    image_path = os.path.join(img_directory, filename)
    return image_path


@tweetBp.route("/image/<string:name>", strict_slashes=False)
@jwt_required(locations=["headers"], optional=True)
def get_image(name):
    image_name = name
    img = serve_image(image_name)
    return send_file(img)


@tweetBp.route("/download/<string:name>", strict_slashes=False)
@jwt_required(locations=["headers"], optional=True)
def download_image(name):
    return send_from_directory(UPLOAD_FILE_LOCATION, name)
