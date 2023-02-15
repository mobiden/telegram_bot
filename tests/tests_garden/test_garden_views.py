import pytest



class Test_FloraTypeAddView:

    async def test_unauthorized(self, cli_without_tel_api):
        test_request = {}
        test_answer = {'data': {}, 'message': "There isn't token", 'status': 'unauthorized'}
        response = await cli_without_tel_api.post('/flora.type_add', json=test_request)
        assert response.status == 401
        answer = await response.json()
        assert  answer == test_answer

    async def test_success_authorized(self, cli_without_tel_api):
        pass