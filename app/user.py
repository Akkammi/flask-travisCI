from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.exc import IntegrityError

from app.db import User, db
from app.schemas import user_schema

bp = Blueprint("user", __name__, url_prefix="/users")


@bp.route("/", methods=["POST"])
def register():
    """
    Реєстрація користувача
    ---
    tags:
        - коритувач
    produces:
        - application/json
    parameters:
        - name: body
          in: body
          description: Дані користувача
          required: true
          schema:
            $ref: '#/definitions/UserIn'
    responses:
        201:
            description: Створено користувача
            schema:
                $ref: '#/definitions/UserOut'
        400:
            description: Помилка валідації
        422:
            description: Помилка валідації
    """
    json_data = request.json
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422

    try:
        new_user = User(
            username=data["username"],
            password=generate_password_hash(data["password"], method="pbkdf2"),
        )
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify(error="Користувач з таким username вже існує!"), 400
    return jsonify(user_schema.dump(new_user)), 201


@bp.route("/login", methods=["POST"])
def login():
    """
    Логін користувача
    ---
    tags:
        - коритувач
    produces:
        - application/json
    parameters:
        - name: body
          in: body
          description: Дані користувача
          required: true
          schema:
            $ref: '#/definitions/UserIn'
    responses:
        200:
            description: Успішний логін
            schema:
                $ref: '#/definitions/TokenOut'
        401:
            description: Не правильний username або password
        404:
            description: Не знайдено користувача
            schema:
                $ref: '#/definitions/NotFound'
        422:
            description: Помилка валідації
    """
    json_data = request.json
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422

    user = db.first_or_404(db.select(User).filter_by(username=data["username"]))

    if not check_password_hash(user.password, data["password"]):
        return jsonify(error="Не правильний username або password!"), 401

    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token)
