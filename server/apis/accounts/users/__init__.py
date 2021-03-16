# Created users.__init__.py by KimDaeil on 03/31/2018

from core.server.apis.common.resource import *
from core.server.apis.common.exceptions import *
from core.server.utils.validations.data import *

from core.models.users import UserModel
from . import post, put, delete


class User(BaseResource):
    def post(self, *args, **kwargs):
        creator = ApiCreator()
        creator.add(validate_function)
        creator.add(post.validate_user_data)
        creator.add(post.create_session)
        creator.add(post.save)
        # creator.add(post.send_auth_mail())
        result = creator.run(
            key=post.essential,
            keys=post.keys,
            nullable=post.nullable,
            validation_function=post.validation_function,
            **kwargs
        )

        return result

    @session_validator()
    def put(self, *args, **kwargs):
        kwargs["is_put"] = True
        creator = ApiCreator()
        creator.add(validate_function)
        creator.add(put.update_user)
        result = creator.run(
            key=put.essential,
            keys=put.keys,
            nullable=put.nullable,
            validation_function=put.validation_function,
            **kwargs
        )

        return result

    @session_validator()
    def delete(self, *args, **kwargs):
        creator = ApiCreator()
        creator.add(validate_function)
        creator.add(delete.delete_user)
        creator.add(delete.delete_session)
        result = creator.run(
            key=delete.essential,
            keys=delete.keys,
            nullable=delete.nullable,
            validation_function=delete.validation_function,
            **kwargs)
        return result
