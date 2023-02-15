import pytest

from app.admin.models import AdminModel


class Test_AdminLoginView:

    #@pytest.mark.parametrize(
    #    'test_request, test_answer, status',
     #                   (
    #            ({"email": "",  "password": ""},
     #            {'data': {}, 'message': 'Unauthorized', 'status': 'unauthorized'}, 403)
      #                  )
       #                         )

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


    async def test_success(self, cli_without_tel_api):
        pass