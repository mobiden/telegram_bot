import uuid

import pytest

from app.admin.models import AdminModel
from tests.conftest import authenticate


class Test_AdminLoginView:


    async def test_unsuccess(self, cli_without_tel_api):
        test_request = {"email": "email@emai.l", "password": "false_password"}
        test_answer = {'status': 'forbidden', 'message': 'Wrong email or password', 'data': {}}
        status = 403

        response = await cli_without_tel_api.post(
            "/admin.login",
            json=test_request,
        )
        assert response.status == status
        answer = await response.json()
        assert answer == test_answer


    async def test_success(self, cli_without_tel_api, admin: AdminModel, mocker):
        test_request = {"email": admin.email, "password": "1234"}
        test_answer = {'data': {'token': '00000000000000000000000000000000'}, 'status': 'ok'}
        token = "0" * 32

        async with authenticate(cli_without_tel_api, admin):
            mock_uuid = mocker.patch.object(uuid, "uuid4", autospec=True)
            mock_uuid.return_value = uuid.UUID(hex=token)
            response = await cli_without_tel_api.post("/admin.login", json=test_request)
        assert response.status == 200
        assert await response.json() == test_answer