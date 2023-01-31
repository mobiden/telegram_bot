import pytest

class Test_FloraTypeAddView:
    test_request = None
    test_answer = None

    @pytest.mark.parametrize("test_request, test_answer", ([test_request, test_answer], ))
    async def test_success(self, cli, test_request, test_answer):
        response = await cli.get('/flora.type_add', json=test_request)
        assert response.status == 200
        assert await response.json() == test_answer