# Created users.post.py by KimDaeil on 03/31/2018
from core.server.utils.validations.user import *

from core.models.sessions import SessionModel
from . import InternalServerErrorException
from . import UserModel
from . import validate_str, validate_int

essential = ["uid", "password", "birthYear", "birthMonth", "birthDay", "gender", "salt", "remote_addr", "remote_platform", "remote_platform_version"]
keys = ["uid", "password", "birthYear", "birthMonth", "birthDay", "gender", "salt", "remote_addr", "remote_platform", "remote_platform_version"]
nullable = []
validation_function = {
    "uid": lambda x: validate_uid(x),
    "password": lambda x: validate_str(x, 1, 128),
    "birthYear": lambda x: validate_int(x, min=1970, max=datetime.now().year, raise_value=1970),
    "birthMonth": lambda x: validate_int(x, max=12, raise_value=0),
    "birthDay": lambda x: validate_int(x, max=31, raise_value=0),
    "gender": lambda x: validate_gender(x),
    "salt": lambda x: validate_str(x, 2, 128),
    "remote_addr": lambda x: x,
    "remote_platform": lambda x: x,
    "remote_platform_version": lambda x: x
}


# 가입 타입 및 조건에 맞게 데이터 파싱: 현재는 없음..ㅋㅋㅋ
# 소셜이나 전번 가입 시
def validate_user_data(data):
    print(" ==== USERS")

    user = UserModel.find_by_email(data["uid"])
    if user.id:
        print("{}.{} >> ".format(__name__, "validate_user_data"), "existing email as uid")
        raise UnauthorizedException()

    user.uid = data["uid"]
    user.password = encryption_password(data.get("password", None))
    user.salt = encryption_salt(data.get("salt", None))

    user.birth_year = data["birthYear"]
    user.birth_month = data["birthMonth"]
    user.birth_day = data["birthDay"]
    user.gender = data["gender"]

    validate_birth_date(user.birth_year, user.birth_month, user.birth_day)

    result = {"user": user,
              "remote_addr": data["remote_addr"],
              "remote_platform": data["remote_platform"],
              "remote_platform_version": data["remote_platform_version"]
              }

    return result


def create_session(data):
    print(" ==== SESSIONS")

    user = data["user"]
    session = SessionModel()
    session.salt = make_session_salt(user.salt)
    session.ip_address = data["remote_addr"]
    session.platform = data.get("remote_platform", "") or ""
    session.platform_version = data.get("remote_platform_version", "") or ""

    data["session"] = session

    return data


def save(data):
    result = {}
    user = data["user"]
    user.save()

    print("session.save: user", user.to_json())
    session = data["session"]
    session.id = user.id
    session.session = session.generate_session(user.id, session.ip_address, session.salt)
    session.save()

    result["user"] = user.to_json()
    result["user"]["session"] = session.to_json()
    return result


# auth by email
def send_auth_mail(data):
    result = {}

    return result
