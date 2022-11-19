from typing import Optional

from app.store.telegram_api.te_dataclasses import InlineKeyboardBottomClass, OutMessage, InlineMarkupClass, \
    ReplyKeyboardBottomClass, ReplyMarkupClass
from app.store.telegram_api.te_schemes import InlineKeyboardMarkupSchema, ReplyKeyboardMarkupSchema


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
