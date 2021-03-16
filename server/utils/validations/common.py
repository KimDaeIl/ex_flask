# Created validator.py by KimDaeil on 04/03/2018
import functools
import json
import json.decoder as json_decoder

from core.models.mongos.sessions import SessionMongo
from core.models.sessions import SessionModel
from core.server.utils.common.security import AESCipher
from flask import request

from core.server.apis.common.exceptions import *


def validator_decorator(*args, **kwargs):
    def validator_wrapper(func):
        @functools.wraps(func)
        def validator(*args, **kwargs):

            """
            will need to handle resettable data if it added like state message etc.
            """

            data = request.form.to_dict()
            data.update(request.args.to_dict())
            data.update(kwargs)

            try:
                # pass True as silent to request.get_json()
                # then, return None if it has not anything
                json_data = request.get_json(silent=True)

                if json_data:
                    data.update(json_data)

            except json_decoder.JSONDecodeError as e:
                print("validator_decorator: json_decoder.JSONDecodeError >> ", e)
                raise UnauthorizedException()

            # update for remote_addr, platform
            data.update({
                "remote_addr": request.remote_addr,
                "remote_platform": request.user_agent.version,
                "remote_platform_version": request.user_agent.platform
            })

            need_keys = kwargs.get("key")
            for k in need_keys:
                if k not in data or data[k] == "":
                    print("key >>", k)
                    print("data >>", data)
                    raise UnauthorizedException()

            return func(*args, status="200", data=data)

        return validator

    return validator_wrapper


def session_validator():
    def validator_wrapper(func):
        @functools.wraps(func)
        def check_session(*args, **kwargs):
            client = request.headers.get("Authorization")

            # 1. check header has 'Authorization' as client access token
            if client is None or len(client) == 0:
                raise UnauthorizedException(attribute="default", details="default")

            # find by session from client
            session = SessionMongo.find_by_session(client)

            # if not in server, then raise error as a result of return
            if "id" not in session or session["id"] == 0:
                print("session_validator >> session is not in mongo server")
                raise UnauthorizedException(attribute="default", details="default")

            server = session.get("session", "")
            if len(server) != len(client):
                print("session_validator >> invalid session")
                raise UnauthorizedException(attribute="default", details="user_info")

            # check ip address on session is equal with client ip.
            if session.get("ipAddress", "") != request.remote_addr:
                print("session_validator >> different ip")
                raise UnauthorizedException(attribute="default", details="user_info")

            kwargs.update({"user_id": session.get("id", 0)})
            # # check session to valid
            # if session is None or len(session) == 0:
            #     raise UnauthorizedException(attribute="default", details="default")
            #
            # # parse to validate
            # session_list = AESCipher().decrypt(session).split("_")
            #
            # # 1-1. length validation
            # if len(session_list) != 3:
            #     raise UnauthorizedException(attribute="default", details="user_info")
            #
            # # 1-2. first value of session_list is id for user
            # # parse string to int
            # try:
            #     user_id = int(session_list[0])
            # except ValueError as e:
            #     raise UnauthorizedException(attribute="default", details="user_info")
            #
            # # 2. is id valid number?
            # if kwargs.get("user_id", 0) != user_id:
            #     raise UnauthorizedException(attribute="default", details="user_info")
            #
            # # 3. find session in NoSQL and parse to equal
            # sessions = SessionMongo.find_by_id(user_id)
            #
            # # invalid session data
            # if len(sessions) == 0:
            #     sessions = SessionModel.find_by_id(user_id)
            #
            #     if sessions.id != 0:
            #         sessions = SessionMongo.create_session(sessions.to_json(has_salt=True))
            #
            #     else:
            #         raise UnauthorizedException(attribute="default", details="user_info")
            #
            # # parse session data on sessions
            # server_session = sessions.get("session", "")
            #
            # if len(server_session) != len(session):
            #     raise UnauthorizedException(attribute="default", details="user_info")
            #
            # for s, u in zip(server_session, session):
            #     if s != u:
            #         raise UnauthorizedException(attribute="default", details="user_info")
            #         break

            return func(*args, **kwargs)

        return check_session

    return validator_wrapper
