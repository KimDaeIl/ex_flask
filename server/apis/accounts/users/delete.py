# Created users.delete.py by KimDaeil on 03/31/2018
from datetime import datetime

from core.models.sessions import SessionModel
from . import UserModel
from . import validate_int
from . import UnauthorizedException, NotFoundException

essential = ["user_id"]
keys = ["user_id"]
nullable = []
validation_function = {
    "user_id": lambda x: validate_int(x, raise_value=0)
}


def delete_user(data):
    print("delete_user")
    result = {}

    user = UserModel.find_by_id(data.get("user_id", 0))

    if not user or not user.id:
        print("users.delete.delete_user >> ", "invalid user information")
        raise UnauthorizedException()

    user.deleted_at = datetime.now()
    user.save()
    result["user"] = user.to_json()

    return result


def delete_session(data):
    session = SessionModel.find_by_id(data["user"]["id"])

    if session and session.id:
        session.delete()
        data["user"]["session"] = session.to_json()

    return data
