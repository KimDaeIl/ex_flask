# Created post.py by KimDaeil on 04/28/2018

from . import UserModel, SessionModel
from core.server.utils.common.security import make_session_salt

from . import NotFoundException, UnauthorizedException
from . import encryption_password, encryption_salt, validate_uid, validate_str

essential = ["uid", "password", "remote_addr", "remote_platform", "remote_platform_version", "remote_addr", "remote_platform", "remote_platform_version"]
keys = ["uid", "password", "remote_addr", "remote_platform", "remote_platform_version", "remote_addr", "remote_platform", "remote_platform_version"]
nullable = []
validation_function = {
    "uid": lambda x: validate_uid(x),
    "password": lambda x: validate_str(x, 1, 128),

    "remote_addr": lambda x: x,
    "remote_platform": lambda x: x,
    "remote_platform_version": lambda x: x
}


def find_user(data):
    print("session.post.find_user.data >> ", data)

    result = {
        "remote_addr": data["remote_addr"],
        "remote_platform": data["remote_platform"],
        "remote_platform_version": data["remote_platform_version"]
    }

    user = UserModel.find_by_email(data.get("uid", ""))

    if not user or not user.id:
        print("session.post.find_user.data ", "not found user information")
        raise UnauthorizedException()

    # ! ---------------
    user_password = encryption_password(data.get("password", None))

    if len(user_password) != len(user.password):
        print("{}.{} >> ".format(__name__, "find_user"), "incorrect password")
        raise UnauthorizedException()

    for p, u in zip(user_password, user.password):
        if p != u:
            print("{}.{} >> ".format(__name__, "find_user"), "incorrect password")
            raise UnauthorizedException()
    # ! ---------------
    result["user"] = user.to_json(has_salt=True)

    return result


def create_session(data):
    result = {}

    user = data["user"]
    session = SessionModel.find_by_id(user["id"])

    if not session.id:
        session.id = user["id"]

    session.session = session.generate_session(user["id"], session.ip_address, session.salt)
    session.salt = make_session_salt(user["salt"])
    session.ip_address = data["remote_addr"]
    session.platform = data.get("remote_platform", "") or ""
    session.platform_version = data.get("remote_platform_version", "") or ""

    session.save()

    result["user"] = user
    result["user"]["session"] = session.to_json()

    return result
