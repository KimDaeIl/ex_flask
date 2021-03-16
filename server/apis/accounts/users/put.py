# Created users.put.py by KimDaeil on 03/31/2018


from core.models.users import UserModel
from core.server.utils.validations.user import *
from . import validate_int
from . import NotFoundException, BadRequestException, UnauthorizedException

essential = ["user_id"]
keys = ["birthYear", "birthMonth", "birthDay", "user_id"]
nullable = ["birthYear", "birthMonth", "birthDay"]
validation_function = {
    "user_id": lambda x: validate_int(x, raise_value=0),
    "birthYear": lambda x: validate_int(x, min=1970, max=datetime.now().year, raise_value=1970),
    "birthMonth": lambda x: validate_int(x, max=12, raise_value=0),
    "birthDay": lambda x: validate_int(x, max=31, raise_value=0)
}


def update_user(data):
    result = {}

    user = UserModel.find_by_id(data.get("user_id", 0))

    if not user or not user.id:
        print("user.put.validate_user_data >> ", "invalid user data")
        raise UnauthorizedException()

    is_update = False
    if "birthYear" in data:
        if user.birth_year != data["birthYear"]:
            user.birth_year = data["birthYear"]
            is_update = True

    if "birthMonth" in data:
        if user.birth_month != data["birthMonth"]:
            user.birth_month = data["birthMonth"]
            is_update = True

    if "birthDay" in data:
        if user.birth_day != data["birthDay"]:
            user.birth_day = data["birthDay"]
            is_update = True

    if not is_update:
        print("user.put.validate_user_data >> ", "update not thing. request same data.")
        raise UnauthorizedException()

    validate_birth_date(user.birth_year, user.birth_month, user.birth_day)

    user.save()
    result["user"] = user.to_json()

    return result
