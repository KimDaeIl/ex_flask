# Created __init__.py.py by KimDaeil on 05/17/2018

from core.server.apis.common.resource import *
from core.server.apis.common.exceptions import *

from . import put


class PushToken(BaseResource):
    @session_validator()
    def put(self, *args, **kwargs):
        kwargs["is_put"] = True
        api = ApiCreator()
        api.add(put.validate)
        api.add(put.update_token)
        result = api.run(
            key=["user_id"],
            req=request,
            **kwargs
        )

        return result
