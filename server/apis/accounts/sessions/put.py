# Created put.py by KimDaeil on 04/28/2018

from datetime import datetime

from core.server.utils.common.security import AESCipher
from . import SessionModel, UserModel
from . import validate_int
from . import UnauthorizedException, NotFoundException

essential = ["user_id"]
keys = ["user_id"]
nullable = []
validation_function = {
    "user_id": lambda x: validate_int(x, raise_value=0)
}


def update_session(data):
    result = {}

    session = SessionModel.find_by_id(data.get("user_id", 0))

    if not session or not session.id:
        print("{}.{} >> ".format(__name__, "update_session"), "not found session")
        raise UnauthorizedException()

    session.updated_at = datetime.now()

    result["session"] = session

    return result


def find_user(data):
    result = {}
    session = data["session"]
    user = UserModel.find_by_id(session.id)

    if not user or not user.id:
        print("{}.{} >> ".format(__name__, "find_user"), "not found user")

        session.delete()
        raise UnauthorizedException()

    session.save()
    result["user"] = user.to_json()
    result["user"]["session"] = session.to_json()

    return result
