# Created models.__init__.py by KimDaeil on 03/31/2018

import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from copy import deepcopy

from . import *

__all__ = ["datetime", "inspect", "db", "String", "Int", "DateTime", "Time", "BigInt", "Bool", "Float"]

db = SQLAlchemy()


class BaseColumn(db.Column):
    def params(self, *optionaldict, **kwargs):
        return self._params(False, optionaldict, kwargs)

    def unique_params(self, *optionaldict, **kwargs):
        return self._params(True, optionaldict, kwargs)

    def __init__(self, *args, **kwarg):
        if 'nullable' not in kwarg:
            kwarg['nullable'] = False

        # if len(args) > 0:
        #     name = args[0]
        #
        #     if isinstance(name, str):
        #         kwarg["name"] = name
        super().__init__(*args, **kwarg)

    @property
    def _constructor(self, *args, **kwargs):
        return BaseColumn


class String(BaseColumn):
    def __init__(self, name, length=0, **kwargs):
        if length == 0:
            length = None

        super().__init__(name, db.String(length), **kwargs)


class Bool(BaseColumn):
    def __init__(self, name, **kwargs):
        if "default" not in kwargs:
            kwargs["default"] = True
        super().__init__(name, db.Boolean, **kwargs)


class Int(BaseColumn):
    def __init__(self, name, **kwargs):
        super().__init__(name, db.Integer, **kwargs)


class BigInt(BaseColumn):
    impl = db.BigInteger

    def __init__(self, name, **kwargs):
        super().__init__(name, db.BigInteger, **kwargs)


class DateTime(BaseColumn):
    def __init__(self, name, **kwargs):
        # TODD 2018. 04. 17. make sure that is timezone
        # consider below terms
        # 1. making time zone about server and user
        # 2. make time zone about server

        if 'default' not in kwargs:
            kwargs['default'] = datetime.datetime.now()

        if 'server_default' not in kwargs:
            from sqlalchemy.sql import func

            kwargs['server_default'] = func.now()

        super().__init__(name, db.DateTime, **kwargs)


class Time(BaseColumn):
    def __init__(self, name, **kwargs):
        super().__init__(name, db.Time, **kwargs)


class Float(BaseColumn):
    def __init__(self, name, precision=None, scale=None, **kwargs):
        if "default" not in kwargs:
            kwargs["default"] = 0.0

        super().__init__(name, db.Numeric(precision=precision + scale, scale=scale, asdecimal=False), **kwargs)


seq_users_id = db.Sequence("seq_users_id", start=1, minvalue=0, increment=1, cache=10, cycle=True, metadata=db.Model.metadata)
