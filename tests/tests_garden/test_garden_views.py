import uuid

import pytest
from pytest_mock import mocker

from app.admin.models import AdminModel
from tests.conftest import authenticate


class Test_FloraTypeAddView:

    async def test_unauthorized(self, cli_without_tel_api):
        test_request = {}
        test_answer = {'data': {}, 'message': "There isn't token", 'status': 'unauthorized'}
        response = await cli_without_tel_api.post('/flora.type_add', json=test_request)

        assert response.status == 401
        answer = await response.json()
        assert  answer == test_answer


    async def test_success_add(self, cli_without_tel_api, admin: AdminModel, mocker):
        test_request = {'flora_type': 'abcdef'}
        test_answer = {"status": "ok","data": {"flora_type": "abcdef"}}

        token = "0" * 32

        async with authenticate(cli_without_tel_api, admin):
            mock_uuid = mocker.patch.object(uuid, "uuid4", autospec=True)
            mock_uuid.return_value = uuid.UUID(hex=token)
            response = await cli_without_tel_api.post("/flora.type_add", json=test_request)
        assert response.status == 200
        assert await response.json() == test_answer