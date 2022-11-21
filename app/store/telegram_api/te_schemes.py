from marshmallow import Schema, fields
from marshmallow.fields import Nested



class ReplyKeyboardBottomSchema(Schema):
    text = fields.Str(required=True)
    request_contact = fields.Bool(required=False)
    request_location = fields.Bool(required=False)


class ReplyKeyboardMarkupSchema(Schema):
    keyboard = fields.List(Nested(ReplyKeyboardBottomSchema, many=True))
    resize_keyboard = fields.Bool(required=False)
    one_time_keyboard = fields.Bool(required=False)
    selective = fields.Bool(required=False)



class InlineKeyboardBottomSchema(Schema):
    text = fields.Str(required=True)
    url = fields.Str(required=False)
    callback_data = fields.Str(required=False)
    switch_inline_query = fields.Str(required=False)
    switch_inline_query_current_chat = fields.Str(required=False)


class InlineKeyboardMarkupSchema(Schema):
    inline_keyboard = fields.List(Nested(InlineKeyboardBottomSchema, many=True))


class UpdateSchema(Schema):
    update_id = fields.Int(required=True)
    message = fields.Str(required=False)
    inlineQuery = fields.Str(required=False)
    chosenInlineResult = fields.Str(required=False)
    callbackQuery = fields.Str(required=False)