from datetime import datetime
from core.server.apis.common.exceptions import *


def has_data_in_dict(dictionary, key):
    if dictionary is not None and key is not None:
        if key in dictionary and dictionary[key] is not None:
            return True

    return False


def has_any_in_set_(keys, data):
    if keys is not None and data is not None:
        if isinstance(keys, set) and isinstance(data, set):
            return any(keys & data)

    return False


def validate_datetime(date):
    print("validate_datetimew ", date)

    try:
        if date is not None and len(date) > 0:
            try:
                value = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                return value
            except ValueError as e:
                raise BadRequestException()

        else:
            datetime.strptime(None)

    except TypeError:
        raise BadRequestException("default", "default")


def validate_date(date):
    print("validate_date ", date)
    try:
        if date is not None and len(date) > 0:
            try:
                value = datetime.strptime(date, "%Y-%m-%d")
                return value
            except ValueError:
                raise BadRequestException()

        else:
            datetime.strptime(None)

    except TypeError:
        print("validate_date")
        raise UnauthorizedException("default", "default")


def validate_str(data, min=1, max=256):
    if data is None or not isinstance(data, str):
        raise BadRequestException("default", "default")

    if min <= len(data) <= max:
        return data
    else:
        print(data)
        raise BadRequestException("default", "default")


def validate_int(data, min=0, default=0, max=None, raise_value=None):
    if data is not None:

        try:
            if not isinstance(data, int):
                data = int(data)

            if data < min:
                data = min

            if max and max < data:
                print("app.server.utils.validations.common.validate_int", "exceed max")
                raise UnauthorizedException()
        except TypeError as e:
            data = default
        except ValueError:
            data = default
            raise_value = default

    else:
        data = default

    if raise_value is not None:
        if data == raise_value:
            print("app.server.utils.validations.common.validate_int >> data: {} / raise value: {}".format(data, raise_value))
            raise UnauthorizedException()

    return data


def validate_float(data, min=0.0, default=0.0, raise_value=None):
    print("validate_float", data)
    if data is not None:
        try:
            if not isinstance(data, float):
                data = float(data)

            if data < min:
                data = min

        except TypeError as e:
            data = default
        except ValueError:
            raise_value = default
            data = default

    else:
        data = default

    if raise_value is not None:
        if data == raise_value:
            print("app.server.utils.validations.common.validate_float >> data: {} / raise value: {}".format(data, raise_value))
            raise UnauthorizedException()

    return data


def validate_list_with_type(data, cls_type, raise_exception=False):
    result = []
    if data is not None:
        if isinstance(data, list) and len(list(filter(lambda x: isinstance(x, cls_type), data))) == len(data):
            result = data

    if not result and raise_exception:
        print("validate_list_with_type", "invalid data")
        raise UnauthorizedException()

    return result


def validate_bool(data):
    if data and isinstance(data, str):
        data = data.lower()
        if data in ["true", "false", "t", "f"]:
            return data[0] == 't'

    print("validate_bool >> invalid: {}".format(data))
    raise UnauthorizedException()


def validate_time(time):
    try:
        if time is not None and len(time) > 0:
            value = datetime.strptime(time, "%H:%M:%S").time()
            return value

        else:
            datetime.strptime(None)

    except TypeError:
        print("validate_time.TypeError >> TypeError: {}".format(time))
        raise UnauthorizedException()

    except ValueError:
        print("validate_time.ValueError >> ValueError: {}".format(time))
        raise UnauthorizedException()


def validate_function(data):
    print("validate_function: data >>", data)
    is_put = data.get("is_put", False)
    keys = data.get("keys", [])
    nullable = data.get("nullable", [])
    validation_function = data.get("validation_function", {})

    if not data or not keys or not validation_function:
        print("validate", "invalid  data or keys or validation_function")
        raise UnauthorizedException()

    result = {}

    for key in keys:
        value = None

        if key in data:
            print("validate_function: key", key)
            value = validation_function.get(key, lambda x: x)(data[key])
        else:

            if key in nullable:
                if is_put:
                    continue
            else:
                print("validate", "key not in data and nullable >> {}".format(key))
                raise UnauthorizedException()

        result[key] = value

    print("validate: result >> ", result)
    if is_put:
        nullable_keys = set(nullable)
        if nullable_keys and not any(result.keys() & nullable_keys):
            print("validate", "empty data to update")
            raise UnauthorizedException()

    return result
