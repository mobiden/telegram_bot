from marshmallow import Schema, fields

# TODO: add validations


class FloraAddSchema(Schema):
    name = fields.Str(required=True)
    type = fields.String(required=True)
    planting_time = fields.Str(required=False)
    harvest_time = fields.Str(required=False)


class FloraTypeAddSchema(Schema):
    id = fields.Int(required=False)
    type = fields.Str(required=True)
