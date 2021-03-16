# Created accounts.__init__.py by KimDaeil on 03/31/2018
from . import *
from flask import Blueprint
from flask_restful import Api
from .sessions import Session
from .users import User
from .email import CheckEmail
from .notifications import Notifications
from .push_token import PushToken

__all__ = ["users_blue_print"]

users_blue_print = Blueprint("users", __name__, url_prefix="/users")
api = Api(users_blue_print)

api.add_resource(User, "", endpoint="user_default")
api.add_resource(User, "/<int:user_id>", endpoint="user_with_id")

api.add_resource(Session, "/sessions", endpoint="session")
api.add_resource(Session, "/sessions/<int:user_id>", endpoint="session_with_id")

api.add_resource(CheckEmail, "/checkEmails/<string:email>", endpoint="check_email")

api.add_resource(Notifications, "/<int:user_id>/notifications")

api.add_resource(PushToken, "/<int:user_id>/push")
