from typing import Optional

from aiohttp.web_urldispatcher import View
from aiohttp_apispec import request_schema

from app.store.telegram_api.te_dataclasses import InlineKeyboardBottomClass, OutMessage, InlineMarkupClass, \
    ReplyKeyboardBottomClass, ReplyMarkupClass
from app.store.telegram_api.te_schemes import InlineKeyboardMarkupSchema, ReplyKeyboardMarkupSchema
from app.store.telegram_api.te_schemes import UpdateSchema

class InlineBottom():
    @staticmethod
    async def create(bott_list: Optional[list] = None) -> dict:
        inline_keyboard = []
        for bottom in bott_list:
            ib = InlineKeyboardBottomClass(text=str(bottom[0]), callback_data=str(bottom[1]))
            inline_keyboard.append(ib)
        mb = InlineMarkupClass(inline_keyboard=[inline_keyboard])
        markup_json = InlineKeyboardMarkupSchema().dump(mb)
        return markup_json

class ReplyKeyboard():
    @staticmethod
    async def create(bott_list: list) -> dict:
        reply_keyboard = []
        for bottom in bott_list:
            rb = ReplyKeyboardBottomClass(text=str(bottom))
            reply_keyboard.append(rb)
        mb = ReplyMarkupClass(keyboard=[reply_keyboard], resize_keyboard=True, one_time_keyboard=True)
        markup_json = ReplyKeyboardMarkupSchema().dump(mb)
        return markup_json


async def create_message(chat_id: str, text:str, markup_json:Optional[dict] = {}) -> OutMessage:
        outmessage = OutMessage(
                    chat_id=chat_id,
                    text=text,
                    reply_markup= markup_json,
                                   )
        return outmessage

class Webhook_handling(View):
    @request_schema(UpdateSchema)
    async def post(self):
        name = self.data["name"]