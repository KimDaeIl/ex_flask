from . import UserModel
from . import SessionModel
from . import validate_int, validate_uid
from . import UnauthorizedException, NotFoundException
from . import decryption_data

essential = ["user_id"]
keys = ["user_id"]
nullable = []
validation_function = {
    "user_id": lambda x: validate_int(x, raise_value=0),
}


def validate_request(data):
    user = UserModel.find_by_id(data.get("user_id", 0))

    if not user.id:
        print("{}.{} >> ".format(__name__, "validate_request"), "not found user")
        raise UnauthorizedException()

    if not user.salt:
        print("{}.{} >> ".format(__name__, "validate_request"), "not fount logged in data")
        raise UnauthorizedException()

    session = SessionModel.find_by_id(user.id)

    if not session or not session.id:
        print("{}.{} >> ".format(__name__, "validate_request"), "invalid session")
        raise UnauthorizedException()

    print(user.to_json(has_salt=False))
    result = {"user": user.to_json(has_salt=False)}
    result["user"].update({"session": session.to_json()})

    return result
