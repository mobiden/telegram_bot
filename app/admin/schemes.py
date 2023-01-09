from marshmallow import Schema, fields


class AdminSchema(Schema):
    id = fields.Int(required=False)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    debug = fields.Boolean(required=False, load_only=True)


class RegisterSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class LoginSchema(Schema):
    adm_sess_token = fields.Str(required=True)
