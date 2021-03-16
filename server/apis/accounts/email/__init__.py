# Created __init__.py.py by KimDaeil on 05/15/2018
from core.server.apis.common.resource import *
from core.server.apis.common.exceptions import *

from . import get


class CheckEmail(BaseResource):
    def get(self, *args, **kwargs):
        api_creator = ApiCreator()
        api_creator.add(get.validator)
        api_creator.add(get.check_email)
        result = api_creator.run(
            key=["email"],
            req=request,
            **kwargs
        )

        return result
