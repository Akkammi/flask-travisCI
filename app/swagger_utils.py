from flask_swagger import swagger


def build_swagger(app):
    swg = swagger(app)
    swg["info"]["title"] = "Додаток для контролю витрат"
    swg["info"]["version"] = "0.0.1"
    swg["definitions"] = {
        "Hello": {
            "type": "object",
            "discriminator": "helloType",
            "properties": {"message": {"type": "string"}},
            "example": {"message": "Привіт, я твій додаток для контролю витрат!"},
        },
        "ExpenseIn": {
            "type": "object",
            "discriminator": "expenseInType",
            "properties": {
                "title": {"type": "string"},
                "amount": {"type": "number"},
            },
            "example": {
                "title": "Я ваша витрата",
                "amount": 0,
            },
        },
        "ExpenseOut": {
            "allOf": [
                {"$ref": "#/definitions/ExpenseIn"},
                {
                    "type": "object",
                    "properties": {
                        "id": {"type": "number"},
                    },
                    "example": {
                        "id": 0,
                    },
                },
            ],
        },
        "UserIn": {
            "type": "object",
            "discriminator": "userInType",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
            "example": {
                "username": "john_doe",
                "password": "my_password",
            },
        },
        "UserOut": {
            "type": "object",
            "discriminator": "userInType",
            "properties": {
                "id": {"type": "number"},
                "username": {"type": "string"},
            },
            "example": {
                "id": 0,
                "username": "john_doe",
            },
        },
        "TokenOut": {
            "type": "object",
            "discriminator": "tokenOutType",
            "properties": {
                "access_token": {"type": "string"},
            },
        },
        "Unauthorized": {
            "type": "object",
            "discriminator": "unauthorizedType",
            "properties": {"error": {"type": "string"}},
            "example": {"error": "У вас немає доступу"},
        },
        "NotFound": {
            "type": "object",
            "discriminator": "notFoundType",
            "properties": {"error": {"type": "string"}},
            "example": {"error": "Ми не змогли знайти це :("},
        },
    }
    return swg
