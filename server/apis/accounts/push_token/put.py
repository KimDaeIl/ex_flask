# Created put.py by KimDaeil on 05/17/2018
from core.models.users import UserModel

from . import NotFoundException, BadRequestException


def validate(data):
    result = {}
    keys_all = ["user_id", "token"]

    for key in keys_all:
        if key in data:
            result[key] = data[key]

    return result


def update_token(data):
    result = {}

    user = UserModel.find_by_id(data.get("user_id", 0))

    if user.id == 0:
        raise NotFoundException(attribute="user", details="id")

    new_token = data.get("token", "")

    if new_token != "":
        user.push_token = new_token
        result["user"] = user.update_user()

    else:
        result["user"] = user.to_json()

    return result
