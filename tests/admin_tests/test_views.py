from app.admin.models import AdminModel


class test_AdminLoginView:
    async def test_success(self, cli):
        admin = AdminModel.
        response = await cli.post('/admin.login',
                    json={
                        "email": "email@emai.l",
                        "password": "false_password",
                    }
                                  )


class test_GetLoginView:
    pass
