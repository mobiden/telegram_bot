import datetime
import json
import typing
from sqlalchemy.future import select as f_select
from aiohttp import ClientOSError, hdrs
from aiohttp.web_exceptions import HTTPUnprocessableEntity, HTTPException, HTTPClientError, HTTPBadRequest, \
    HTTPUnauthorized
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import get_session
from sqlalchemy import and_

from app.admin.models import AdminModel, Admin_Session
from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request


HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
                    }


def get_token(request: "Request"):
    authorization = request.headers.get(hdrs.AUTHORIZATION)
    if authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0] == "Bearer":
            return parts[1]
    return None


@middleware
async def auth_middleware(request: "Request", handler: callable):
 #   token = get_token(request)
 #   if token:
 #       async with request.app.database.db_async_session() as db_session:
 #           web_session = await db_session.executive(f_select(Admin_Session).where(
 #           and_(
  #              Admin_Session.adm_sess_token == token,
 #               Admin_Session.expires >= datetime.datetime.utcnow(),
#            )
#        ).first())
 #       if web_session:
 #           request["admin_id"] = web_session.admin_id
 #       else:
  #          raise HTTPUnauthorized(reason='Invalid or obsolete token' )
 #  else:
 #       raise HTTPUnauthorized(reason="There isn't token")

    return await handler(request)



@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status="bad_request",
            message=e.reason,
            data=json.loads(e.text),
        )

    except HTTPClientError as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES[e.status],
            message=str(e),
        )

    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES[e.status],
            message=str(e),
        )

    except HTTPUnauthorized as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES[e.status],
            message=str(e),
        )

    except Exception as e:
        request.app.logger.error("Exception", exc_info=e)
        if '_apispec_parser' not in str(e):
            return error_json_response(
                http_status=500, status=f"internal server error. {str(e)}", message=str(e)
            )

        return error_json_response(
            http_status=400, status="HTTPBadRequest", message='Wrong JSON schema'
        )


def setup_middlewares(app: "Application"):
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(auth_middleware)
    app.middlewares.append(validation_middleware)
