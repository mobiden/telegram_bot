import pytest

from app.store.telegram_api.te_view import ReplyKeyboard



class Test_ReplyKeyboard:
    bott_list = ["дерево", "кустарник", "цветок"]
    markup_json = {
        "resize_keyboard": True,
        "selective": False,
        "one_time_keyboard": True,
        "keyboard": [
            [
                {
                    "text": "дерево",
                    "request_contact": False,
                    "request_location": False,
                },
                {
                    "text": "кустарник",
                    "request_contact": False,
                    "request_location": False,
                },
                {
                    "text": "цветок",
                    "request_contact": False,
                    "request_location": False,
                },
            ]
        ],
    }

    @pytest.mark.parametrize(
        "bott_list, markup_json",
                ((bott_list, markup_json),
                )
    )
    async def test_success(self, bott_list, markup_json):
        test_markup_json = await ReplyKeyboard.create(bott_list)
        assert test_markup_json == markup_json



class Test_Webhook_handling:
    request = None
    answer = None

    @pytest.mark.parametrize(
        "request, answer",
        ((request, answer),
         ))
    async def test_success(self, request, answer):
        pass

