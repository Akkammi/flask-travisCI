from flask import Blueprint, Response, request, jsonify
from app.db import db, Expense
from app.schemas import expenses_schema, expense_schema
from marshmallow import ValidationError
from flask_jwt_extended import current_user, jwt_required

bp = Blueprint("expense", __name__, url_prefix="/expense")


@bp.route("/", methods=["POST"])
@jwt_required()
def create_expense():
    """
    Створює нову витрату
    ---
    tags:
        - витрати
    parameters:
        - name: Authorization
          in: header
          description: JWT token
          required: true
        - name: expense
          in: body
          description: Дані витрати
          required: true
          schema:
              $ref: '#/definitions/ExpenseIn'
    responses:
        201:
            description: Створена витрата
            schema:
                $ref: '#/definitions/ExpenseOut'
        401:
            description: Немає доступу
            schema:
                $ref: '#/definitions/Unauthorized'
        422:
            description: Помилка валідації
    """
    json_data = request.json
    try:
        data = expense_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    new_expense = Expense(
        title=data["title"],
        amount=data["amount"],
        user_id=current_user.id,
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify(expense_schema.dump(new_expense)), 201


@bp.route("/", methods=["GET"])
@jwt_required()
def get_expenses():
    """
    Повертає список усіх витрат
    ---
    tags:
        - витрати
    produces:
        - application/json
    parameters:
        - name: Authorization
          in: header
          description: JWT token
          required: true
    responses:
        200:
            description: Список витрат
            schema:
                type: array
                items:
                    $ref: '#/definitions/ExpenseOut'
        401:
            description: Немає доступу
            schema:
                $ref: '#/definitions/Unauthorized'
    """
    # expenses = Expense.query.all()

    # return (
    #     jsonify(
    #         [
    #             {
    #                 "id": expense.id,
    #                 "title": expense.title,
    #                 "amount": expense.amount,
    #             }
    #             for expense in expenses
    #         ]
    #     ),
    #     200,
    # )
    return jsonify(expenses_schema.dump(current_user.expenses)), 200


@bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_expense(id):
    """
    Повертає витрату
    ---
    tags:
      - витрати
    produces:
      - application/json
    parameters:
        - name: Authorization
          in: header
          description: JWT token
          required: true
        - name: id
          in: path
          description: Ідентифікатор витрати
          required: true
          type: number
    responses:
        200:
            description: Знайдено витрату
            schema:
                $ref: '#/definitions/ExpenseOut'
        401:
            description: Немає доступу
            schema:
                $ref: '#/definitions/Unauthorized'
        404:
            description: Не знайдено витрату за ідентифікатором
            schema:
                $ref: '#/definitions/NotFound'
    """
    expense = db.get_or_404(Expense, id)
    if expense.user_id != current_user.id:
        return jsonify(error="У вас немає доступу до ціеї витрати"), 401

    # return jsonify(
    #     {
    #         "id": expense.id,
    #         "title": expense.title,
    #         "amount": expense.amount,
    #     }
    # )
    return jsonify(expense_schema.dump(expense)), 200


@bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_expense(id):
    """
    Оновлює дані витрати за ідентифікатором
    ---
    tags:
        - витрати
    produces:
        - application/json
    parameters:
    - name: Authorization
      in: header
      description: JWT токен
      required: true
    - name: id
      in: path
      description: Ідентифікатор витрати
      required: true
      type: number
    - name: expense
      in: body
      description: Дані для оновлення витрати
      required: true
      schema:
        $ref: '#/definitions/ExpenseIn'
    responses:
        200:
            description: Оновлена витрата
            schema:
                $ref: '#/definitions/ExpenseOut'
        401:
            description: Немає доступу
            schema:
                $ref: '#/definitions/Unauthorized'
        404:
            description: Не знайдено витрату за ідентифікатором
            schema:
                $ref: '#/definitions/NotFound'
        422:
            description: Помилка валідації
    """
    expense = db.get_or_404(Expense, id)

    if expense.user_id != current_user.id:
        return (jsonify(error="У вас немає доступу до цієї витрати")), 401

    json_data = request.json
    try:
        data = expense_schema.load(json_data, partial=True)
    except ValidationError as err:
        return err.messages, 422
    expense.title = data.get("title", expense.title)
    expense.amount = data.get("amount", expense.amount)
    db.session.commit()
    return jsonify(expense_schema.dump(expense)), 200


@bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_expense(id):
    """
    Видаляє витрату за ідентифікатором
    ---
    tags:
        - витрати
    produces:
        - application/json
    parameters:
        - name: Authorization
          in: header
          description: JWT token
          required: true
        - name: id
          in: path
          description: Ідентифікатор витрати
          required: true
          type: number
    responses:
        204:
            description: Успішне видалення витрати
        401:
            description: Немає доступу
            schema:
                $ref: '#/definitions/Unauthorized'
        404:
            description: Не знайдено витрату за ідентифікатором
            schema:
                $ref: '#/definitions/NotFound'
    """
    expense = db.get_or_404(Expense, id)
    if expense.user_id != current_user.id:
        return jsonify(error="У вас немає доступу до ціеї витрати"), 401
    db.session.delete(expense)
    db.session.commit()

    return "", 204
