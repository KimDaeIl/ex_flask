# Created core.__init__.py by KimDaeil on 03/31/2018


def before_first_request():
    from flask import current_app
    from core.server.apis.common.response import BaseResponse

    from core.models import db
    from core.models.mongos import mongo_init_app
    from core.server.apis.common.exceptions import init_error_handler

    print("before_first_request")
    current_app.response_class = BaseResponse

    print("before_first_request >> db_init")
    db.init_app(current_app)
    db.create_all()

    print("before_first_request >> mongo_init")
    mongo_init_app(current_app)

    print("before_first_request >> init_error_handler")
    init_error_handler(current_app)
