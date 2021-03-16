# Created api_creator.py by KimDaeil on 04/01/2018


from flask import current_app

from core.server.utils.validations.common import validator_decorator


class ApiCreator(object):
    def __init__(self):
        self.func_list = []

    def add(self, func):
        if callable(func):
            self.func_list.append(func)

    @validator_decorator()
    def run(self, **kwargs):

        data = kwargs["data"] if kwargs is not None and "data" in kwargs else {}

        while len(self.func_list) > 0:
            func = self.func_list.pop(0)
            data = func(data)

        response = current_app.response_class(data=data)

        return response
