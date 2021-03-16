# Created ㅔㅕㅅ.py by KimDaeil on 05/15/2018
from core.models.users import UserModel
from . import NotFoundException


def validate(data):
    result = {}
    keys_all = ["user_id", "receive_push", "receive_marketing"]

    value = ""
    for key in keys_all:
        if key in data:
            value = data[key]

            if isinstance(value, str):
                if value in ["True", "False", "true", "false", "t", "f"]:
                    value = convert_valid_value(value)

            result[key] = value

    return result


def update_user(data):
    result = {}

    user = UserModel.find_by_id(data.get("user_id", 0))

    if user.id == 0:
        raise NotFoundException("user", "default")

    if "receive_push" in data:
        user.receive_push = data.get("receive_push", True)

    if "receive_marketing" in data:
        user.receive_marketing = data.get("receive_marketing", True)

    result["user"] = user.update_user()

    return result


def convert_valid_value(value):
    return value[0] in ["T", "t"]
