from marshmallow import Schema, fields, validate


class ExpenseSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50),
    )
    amount = fields.Float(
        required=True,
        validate=validate.Range(min=0.01),
    )


expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50),
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=4),
    )


user_schema = UserSchema()
