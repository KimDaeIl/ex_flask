# Created resource.py by KimDaeil on 03/31/2018
from flask_restful import Resource
from core.server.utils.common.api_creator import ApiCreator
from flask import request
from core.server.apis.common.exceptions import MethodNotAllowedException
from core.server.utils.validations.common import session_validator

__all__ = ["BaseResource", "ApiCreator", "request", "session_validator"]


class BaseResource(Resource):
    def post(self, *args, **kwargs):
        raise MethodNotAllowedException(attribute="default", details="default")

    def get(self, *args, **kwargs):
        raise MethodNotAllowedException(attribute="default", details="default")

    def put(self, *args, **kwargs):
        raise MethodNotAllowedException(attribute="default", details="default")

    def delete(self, *args, **kwargs):
        raise MethodNotAllowedException(attribute="default", details="default")

    def options(self, *args, **kwargs):
        raise MethodNotAllowedException(attribute="default", details="default")
