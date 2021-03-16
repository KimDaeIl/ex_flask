# Created resopnse.py by KimDaeil on 04/05/2018

import datetime
import json

from flask import Response, request


class BaseResponse(Response):
    charset = "utf-8"

    def __init__(self, data={}, status="200", mimetype="application/json"):
        response = ResponseData(status, request.method, request.url, data)

        # TODO 2018. 04. 24. save log

        super(Response, self).__init__(response=json.dumps(response()), status=status,
                                       mimetype=mimetype)


class ResponseData:
    def __init__(self, code, method, url, result):
        self.code = code
        self.method = method
        self.url = url
        self.result = result
        self.timestamp = datetime.datetime.now().timestamp()

    def __call__(self, *args, **kwargs):
        return self.__dict__


def parse_error_code(code, error_keyword):
    from core.server.meta import error_code

    error_msg = ""
    if code and error_keyword:
        error_msg = error_code.get_error_message(code, error_keyword)

    return error_msg
