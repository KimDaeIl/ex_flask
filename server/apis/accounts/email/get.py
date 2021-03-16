# Created get.py by KimDaeil on 05/15/2018
from core.models.users import UserModel
from core.server.utils.validations.user import validate_uid
from . import BadRequestException


def validator(data):
    result = {}
    keys_all = ["email"]
    validation_func = {
        "email": lambda x: validate_uid(x)
    }

    for key in keys_all:
        if key in data:
            result[key] = validation_func[key](data[key])

    return result


def check_email(data):
    result = {}

    if "email" not in data:
        raise BadRequestException(attribute="uid", details="default")

    user = UserModel.find_by_email(data["email"])
    result["email"] = data["email"]
    result["usable"] = (user.id == 0)

    return result
