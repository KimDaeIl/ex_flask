# Created error_code.py by KimDaeil on 04/03/2018
from .common import user_meta

error = {
    "4": {
        "uncaught": {
            "default": "잘못된 요청입니다."
        }
    },
    "400": {
        "default": "bed request",
        "uncaught": "잘못된 요청입니다",
        "uid": {
            "default": "email이 없는 데예?",
            "format": "이메일 형식이 맞지 않습니다.",
            "notNullable": "이메일은 초기화할 수 없습니다."
        },
        # "password": {
        #     "default": "비밀번호가 없는데예?",
        #     "format": "비밀번호의 길이는 {0} ~ {1}자, 대문자는 최소 {2}자, 특수문자는 최소 1자에 {3} 만 허용됩니다.".format(
        #         user_meta.get("password").get("minLength"), user_meta.get("password").get("maxLength"),
        #         user_meta.get("password").get("upper_case").get("minLength"),
        #         ", ".join(user_meta.get("password").get("special").get("enum").replace("\\", ""))),
        #     "length": "비밀번호의 길이는 {0} ~ {1}자 입니다".format(user_meta.get("password").get("minLength"),
        #                                                 user_meta.get("password").get("maxLength")),
        #     "special": "허용되는 특수 문자는 [{0}] 입니다".format(
        #         ", ".join(user_meta.get("password").get("special").get("enum").replace("\\", ""))),
        #     "upper": "대문자 최소 {0}자는 포함되어야 합니다.",
        #     "notNullable": "비밀번호은 초기화할 수 없습니다."
        # },
        "birthYear": {
            "default": "생년이 없는데예?",
            "outOfRange": "잘못된 연도입니다.",
            "notNullable": "생년은 초기화할 수 없습니다."
        },
        "birthMonth": {
            "default": "생월이 없는데예?",
            "outOfRange": "잘못된 월 입니다.",
            "outOfNow": "이번 달보다 미래네요?",
            "notNullable": "생월은 초기화할 수 없습니다."
        },
        "birthDay": {
            "default": "생일이 없는데예?",
            "outOfRangeMonth": "입력한 월과 일의 정보를 확인해주세요.",
            "oufOfNow": "오늘보다 미래네요.",
            "notNullable": "생일은 초기화할 수 없습니다."
        },
        "gender": {
            "default": "성별이 없는데예?",
            "format": "입력된 성별 정보를 확인해주세요.",
            "notNullable": "성별은 초기화할 수 없습니다."
        },
        "typeError": {
            "int": "숫자만 입력할 수 있습니다."
        }

    },
    "401": {
        "default": {
            "default": "접근 권한이 없습니다.",
            "user_info": "해당 세션이 유효하지 않습니다.",
            "login": "로그인 정보를 확인해주세요."
        }
    },
    "404": {
        "default": {
            "default": "못 찾음..ㅠㅠ"
        },
        "user": {
            "default": "그런 유저 없는데여?",
            "id": "잘못된 정보인데여?",
            "uid": "그런 아이디없는데여???"
        },
        "session":{
            "default":"해당 접속 정보를 찾을 수 없습니다."
        }
    },
    "405": {
        "default": {"default": "해당 기능 미지원입네다아~"},
        "user": {
            "get": "회원 정보는 지원안해요."
        }
    },
    "500": {
        "default": {
            "default": "내부서버 오류로 실패했습니다 다시 시도 ㄱㄱ",
            "mongodb": "fail to init mongoDB"
        }
    }

}

"""
    400: bad request,
    401: unauthorized
    404: not found
    405: method not allowed
    408: request timeout
    500: internal server error
    503: service unavailable
    """
__allowed_error = ["400", "401", "404", "405", "408", "500", "503"]


def get_400_error_message(code):
    return error.get("400").get(code) if code and code in error.get("400").keys() else error.get("400").get("default")


def get_error_message(code):
    print("error code is {}".format(code))
    if code in __allowed_error:
        return error.get(code).get("default")

    return error.get("400").get("default")


def get_error_message(error_code, keyword):
    if error_code in __allowed_error:
        return error.get(error_code).get(keyword) if keyword and keyword in error.get(error_code).keys() else error.get(
            error_code).get(
            "default")

    return error.get("400").get("default")
