# Created delete.py by KimDaeil on 04/28/2018
from . import SessionModel, UserModel
from . import UnauthorizedException, NotFoundException
from . import validate_int

essential = ["user_id"]
keys = ["user_id"]
nullable = []
validation_function = {
    "user_id": lambda x: validate_int(x, raise_value=0)
}


def delete_session(data):
    result = {}

    session = SessionModel.find_by_id(data.get("user_id", 0))

    if not session.id:
        print("{}.{}".format(__name__, "delete_session"), " not fount session")
        raise UnauthorizedException()

    result["session"] = session

    return result


def update_user(data):
    result = {}
    session = data["session"]
    user = UserModel.find_by_id(session.id)

    if not user or not user.id:
        print("{}.{}".format(__name__, "update_user"), " not fount user")
        raise UnauthorizedException()

    session.delete()

    result["user"] = user.to_json()
    result["user"]["session"] = session.to_json()

    return result
