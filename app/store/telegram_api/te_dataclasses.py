from dataclasses import dataclass, field


# Incoming
from typing import List, Optional


@dataclass
class WriterClass:
    id: int
    is_bot: bool
    username: str
    language_code: str
    title: Optional[str] = field(default='')
    first_name: Optional[str] = field(default='')
    last_name: Optional[str] = field(default='')

@dataclass
class ChatClass:
    id: int
    type: str
    title: Optional[str] = field(default='')
    username: Optional[str] = field(default='')
    first_name: Optional[str] = field(default='')
    last_name: Optional[str] = field(default='')
    all_members_are_administrators: Optional[bool] = field(default=False)

@dataclass
class EntitiesClass:
    offset: int
    length: int
    type: str

@dataclass
class MessageClass:
    message_id: int
    date: int
    text: str
    chat: Optional[ChatClass] = field(default=None)
    from_: Optional[WriterClass] = field(default=None)
    forward_from: Optional[str]= field(default='')
    entities: Optional[EntitiesClass] = field(default=None)


@dataclass
class UpdateClass:
    update_id: int
    message: Optional[MessageClass] = field(default=None)
    inlineQuery: Optional[str]  = field(default='')# переделать
    chosenInlineResult: Optional[str]  = field(default='')# переделать
    callbackQuery: Optional[str]  = field(default='')# переделать


# Outcoming

@dataclass
class ReplyKeyboardBottomClass:
    text: str
    request_contact: Optional[bool] = field(default=False) #направит контакты пользователя
    request_location: Optional[bool] = field(default=False) #направит геолокацию

@dataclass
class InlineKeyboardBottomClass:
    text:str
    url:Optional[str] = field(default='') #URL, который откроется при нажатии на кнопку
    callback_data:Optional[str] = field(default='') #Данные, которые будут отправлены в callback_query при нажатии на кнопку
    switch_inline_query:Optional[str] = field(default='') # Если этот параметр задан, то при нажатии на кнопку приложение предложит пользователю выбрать любой чат, откроет его и вставит
                    # в поле ввода сообщения юзернейм бота и определённый запрос для встроенного режима. Если отправлять пустое поле, то будет вставлен только юзернейм бота.
                    #Примечание: это нужно для того, чтобы быстро переключаться между диалогом с ботом и встроенным режимом с этим же ботом. Особенно полезно в сочетаниями
                    #с действиями switch_pm… – в этом случае пользователь вернётся в исходный чат автоматически, без ручного выбора из списка.
    switch_inline_query_current_chat:Optional[str] = field(default='') #Если установлено, нажатие кнопки вставит имя пользователя бота и указанный встроенный запрос в поле ввода текущего чата.
                    # Может быть пустым, в этом случае будет вставлено только имя пользователя бота.


@dataclass
class InlineMarkupClass:
    inline_keyboard: List[InlineKeyboardBottomClass]

@dataclass
class ReplyMarkupClass:
    keyboard: List[ReplyKeyboardBottomClass]
    resize_keyboard: Optional[bool] = field(default=False) #    Указывает клиенту подогнать высоту клавиатуры под количество кнопок (сделать её меньше, если кнопок мало).
                # По умолчанию False, то есть клавиатура всегда такого же размера, как и стандартная клавиатура устройства.

    one_time_keyboard: Optional[bool] = field(default=False) #Указывает клиенту скрыть клавиатуру после использования (после нажатия на кнопку).
                                                # Её по-прежнему можно будет открыть через иконку в поле ввода сообщения.
    selective: Optional[bool] = field(default=False) # Этот параметр нужен, чтобы показывать клавиатуру только определённым пользователям. Цели: 1) пользователи,
                        # которые были @упомянуты в поле text объекта Message; 2) если сообщения бота является ответом
                        # (содержит поле reply_to_message_id), авторы этого сообщения.



@dataclass
class OutMessage:
    chat_id: int
    text: str
    reply_markup: InlineMarkupClass

