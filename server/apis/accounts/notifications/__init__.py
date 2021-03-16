# Created __init__.py.py by KimDaeil on 05/15/2018
from core.server.apis.common.resource import *
from core.server.apis.common.exceptions import *

from . import put


class Notifications(BaseResource):
    @session_validator()
    def put(self, *args, **kwargs):
        kwargs["is_put"] = True
        api_creator = ApiCreator()
        api_creator.add(put.validate)
        api_creator.add(put.update_user)
        result = api_creator.run(
            key=["user_id"],
            req=request,
            **kwargs
        )

        return result
