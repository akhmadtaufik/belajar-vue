from flask import jsonify, make_response, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

# import flask login
from flask_login import login_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.auth import authBp
from app.extensions import db, jwt
from app.models.blacklist_token import BlacklistToken
from app.models.user import Users


@authBp.route("/register", methods=["POST"], strict_slashes=False)
def registration():
    # get data from request json
    data = request.get_json()
    print(data)
    # get username password email from json
    username = data.get("username", None)
    role = data.get("role", None)
    password = generate_password_hash(data.get("password", None))
    email = data.get("email", None)

    error = None

    # validasi input
    if not username:
        error = "Username is required."
    elif not password:
        error = "Password is required."

    db.session.add(
        Users(username=username, password=password, email=email, role=role)
    )
    db.session.commit()

    # jika terdapat error tampilkan dengan flask
    if error:
        return jsonify({"error": error})

    response = make_response(
        jsonify(
            {
                "message": "Berhasil Login",
            }
        ),
        200,
    )

    return response


@authBp.route("/login", methods=["POST"], strict_slashes=False)
def login():
    # get data from request json
    data = request.get_json()

    # get username password from json
    username = data.get("username", None)
    password = data.get("password", None)

    # validasi input
    if not username:
        error = "Username is required."
    elif not password:
        error = "Password is required."

    error = None
    # query record user dari database dengan username request
    user = db.session.execute(
        db.select(Users).filter_by(username=username)
    ).scalar_one()

    # cek apakah user ada
    if user is None:
        error = "username not found"
    elif not check_password_hash(user.password, password):
        error = "Incorrect password"
    # ditambahkan
    else:
        login_user(user)
        access_token = create_access_token(identity=user.user_id)
        refresh_token = create_refresh_token(identity=user.user_id)

    # jika terdapat error tampilkan dengan flask
    if error:
        return jsonify({"error": error}), 422

    # make response
    response = make_response(
        jsonify(
            {
                "message": "Berhasil Login",
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        ),
        200,
    )
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # jika berhasil berikan message berhasil login
    return response


@authBp.route("/refresh", methods=["POST"])
@jwt_required(locations=["headers"])
def refresh():
    current_user = get_jwt_identity()
    access_token = {"access_token": create_access_token(identity=current_user)}
    return jsonify(access_token), 200


@authBp.route("/logout", methods=["POST"], strict_slashes=False)
@jwt_required(locations=["headers"])
def logout():
    # mendapatkan token jwt
    raw_jwt = get_jwt()
    print(raw_jwt)

    # menambahkan token jwt ke blacklist
    # mencabut JWT dan menolak akses ke permintaan di masa mendatang
    jti = raw_jwt.get("jti")
    token = BlacklistToken(jti=jti)

    db.session.add(token)
    db.session.commit()

    # make response
    response = make_response(jsonify({"message": "Berhasil Logout"}), 200)
    return response


# callback untuk memeriksa apakah JWT ada di daftar blokir atau tidak
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = BlacklistToken.query.filter_by(jti=jti).first()
    return token_in_redis is not None
