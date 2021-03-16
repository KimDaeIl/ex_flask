# Created user.py by KimDaeil on 04/08/2018
import re
from datetime import datetime

from core.server.meta.common import user_meta
from core.server.utils.common.security import AES, AESCipher, make_hashed, make_session_salt

from core.server.apis.common.exceptions import BadRequestException
from core.server.apis.common.exceptions import UnauthorizedException


def validate_uid(uid):
    email_meta = user_meta.get("email")

    if not isinstance(uid, str):
        uid = str(uid)

    if not email_meta.get("minLength") <= len(uid) <= email_meta.get("maxLength"):
        print("validate_uid >> ", "invalid email length")
        raise UnauthorizedException()
    if not bool(re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", uid)):
        print("validate_uid >> ", "invalid email format")
        raise UnauthorizedException()

    return uid


def validate_birth_date(year, month, day):
    print("server.utils.validations.validate_birth_date >> ")
    year = validate_birth_year(year)
    month = validate_birth_month(year, month)
    day = validate_birth_day(year, month, day)

    return year, month, day


def validate_birth_year(year):
    print("server.utils.validations.validate_birth_year >> ", year)

    year_meta = user_meta.get("birthYear")

    if not isinstance(year, int):
        try:
            year = int(year)
        except ValueError:
            raise BadRequestException("typeError", "int")

    if year_meta.get("minLength") > year > datetime.now().year:
        raise BadRequestException("birthYear", "outOfRange")

    return year


def validate_birth_month(year, month):
    print("server.utils.validations.validate_birth_month >> ", year, month)

    month_meta = user_meta.get("birthMonth")

    if not isinstance(month, int):
        try:
            month = int(month)
        except ValueError:
            raise BadRequestException("typeError", "int")

    if month_meta.get("minLength") > month > month_meta.get("maxLength"):
        raise BadRequestException("birthMonth", "outOfRange")

    now = datetime.now()
    if year == now.year and month < now.month:
        raise BadRequestException("birthMonth", "outOfNow")

    return month


def validate_birth_day(year, month, day):
    print("server.utils.validations.validate_birth_day >> ", year, month, day)
    if not isinstance(day, int):
        try:
            day = int(day)
        except ValueError:
            raise BadRequestException("typeError", "int")

    import calendar

    last_day = calendar.monthrange(int(year), int(month))[1]
    if 1 > day > last_day:
        raise BadRequestException("birthYear", "outOfRangeMonth")

    now = datetime.now()
    today = now.day
    if now.year == year and now.month == month and day < today:
        raise BadRequestException("birthDay", "oufOfNow")

    return day


def validate_gender(gender):
    meta = user_meta.get("gender")

    print("validate_gender >> ", gender)
    if gender not in meta.get("enum"):
        raise BadRequestException("gender", "format")

    return gender


def encryption_password(password):
    if not password:
        print("{}.{} >> ".format(__name__, "encryption_password"), "password is invalid")
        raise UnauthorizedException()
    iv = make_hashed(password[:AES.block_size])
    hashed = AESCipher(iv=iv.encode()).encrypt(password)
    hashed = make_hashed(hashed)
    return hashed


def encryption_salt(salt):
    if not salt:
        print("{}.{} >> ".format(__name__, "encryption_salt"), "salt is invalid")
        raise UnauthorizedException()

    return AESCipher().encrypt(salt)


def decryption_data(data, iv=None):
    if not data:
        print("{}.{} >> ".format(__name__, "decryption_data"), "data is invalid")
        raise UnauthorizedException()

    return AESCipher(iv=iv).decrypt(data)
