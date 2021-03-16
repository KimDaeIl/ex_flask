# Created common.py by KimDaeil on 04/03/2018
import datetime

user_meta = {
    "email": {
        "minLength": 10,
        "maxLength": 255
    },
    "gender": {
        "default": "f",
        "enum": ["m", "f"]
    },
    "birthYear": {
        "minLength": 1970
    },
    "birthMonth": {
        "minLength": 1,
        "maxLength": 12
    }

}


# def get_sign_up(code):
#     return user_meta.get("signUp").get(code) \
#         if code and code in user_meta.get("signUp").keys() \
#         else user_meta.get("signUp")
