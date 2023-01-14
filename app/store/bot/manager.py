
import typing
import datetime
from logging import getLogger, DEBUG

from app.store.telegram_api.te_dataclasses import OutMessage, UpdateClass, MessageClass, ChatClass
from app.store.telegram_api.te_view import create_message, InlineBottom, ReplyKeyboard

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.bot = None
        self.logger = getLogger("handler")
        if self.app.config.admin.debug:
            self.logger.setLevel(DEBUG)


    async def handle_updates(self, updates: typing.List[UpdateClass]):
        for update in updates:
            if 'message' in update:
                outmessage = await self.message_processing(update)

            elif 'callback_query' in update:
                outmessage = await self.callback_q_processing(update)

            self.app.store.telegram_api.up_id = update['update_id']
            resp = await self.app.store.telegram_api.send_message(outmessage)
            self.logger.info('handle updates: ', resp)



    async def message_processing(self, update: UpdateClass) -> OutMessage:
        temp_dict = update['message']
        message = MessageClass(
            text=temp_dict['text'],
            message_id= temp_dict['message_id'],
            date= temp_dict['date'],
            chat=ChatClass(
                    id=temp_dict['chat']['id'],
                    type=temp_dict['chat']['type'],
                        )
                            )
        types = await self.app.store.store_flora.list_types()
        flora_names = await self.app.store.store_flora.flora_names_list()
        chat_id = message.chat.id

        if (message.text).lower() in ['/start', '/старт']:
            text = 'Выберите тип растения:'
            markup_json = await ReplyKeyboard.create(types)
            outmessage = await create_message(chat_id=chat_id, text=text,
                                              markup_json=markup_json)
        elif message.text.lower() in types:
            text = 'Выберите растение:'
            filtred_flora = await self.app.store.store_flora.flora_names_list(type=message.text)
            markup_json = await ReplyKeyboard.create(filtred_flora)
            outmessage = await create_message(chat_id=chat_id, text=text,
                                              markup_json=markup_json)
        elif message.text.lower() in flora_names:
            current_month = datetime.datetime.now().strftime('%m')
            list_operations = await self.app.store.store_flora.list_operations(
                                                    flora=message.text.lower())
            text = 'Нет описания на текущий месяц'
            for operation in list_operations:
                if int(operation.operation_time) == int(current_month):
                    text = operation.description
            outmessage = await create_message(chat_id=chat_id, text=text)

        else:
            text = 'Наберите /старт'
            outmessage = await create_message(chat_id=chat_id, text=text)

        return outmessage




    async def callback_q_processing(self, update: UpdateClass) -> OutMessage:
        outmessage = await create_message(field='callback_query', update=update, )
        return outmessage

