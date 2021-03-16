# Created users.py by KimDaeil on 04/14/2018
from datetime import datetime

from core.models import *
from core.models import seq_users_id
from core.server.utils.common.security import make_hashed


class UserModel(db.Model):
    __tablename__ = 'users'

    id = BigInt("id", primary_key=True, index=True, server_default=seq_users_id.next_value())
    uid = String("uid", 255, index=True)
    salt = String("salt", 256)
    password = String("password", 256)
    birth_year = Int("birth_year", default=1970)
    birth_month = Int("birth_month", default=1)
    birth_day = Int("birth_day", default=1)
    push_token = String("push_token", 256, default="", server_default="t")
    receive_push = Bool("receive_push", default=True, server_default="t")
    receive_marketing = Bool("receive_marketing", default=True, server_default="t")
    gender = String("gender", 1, default="f")
    created_at = DateTime("created_at")
    deleted_at = DateTime("deleted_at", nullable=True, server_default=None, default=None)

    __table_agrs__ = (db.UniqueConstraint("uid"),
                      db.Index("idx_users_uid", "uid", postgresql_using="hash"))

    session = None

    def __init__(self, _id=None):
        self.id = _id

    def to_json(self, has_salt=False):
        user = {
            "id": self.id,
            "uid": self.uid,
            "birthYear": self.birth_year,
            "birthMonth": self.birth_month,
            "birthDay": self.birth_day,
            "gender": self.gender,
            "pushToken": self.push_token,
            "push": self.receive_push,
            "marketing": self.receive_marketing,
            "createdAt": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else "",
            "deleted_at": self.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if self.deleted_at else ""
        }

        if has_salt:
            user["salt"] = self.salt

        return user

    def save(self):
        if self.id != 0:
            db.session.add(self)
            db.session.commit()

    # @@ not use
    def create_user(self):
        result = {}

        if self and self.id != 0:
            db.session.add(self)
            db.session.commit()
            result = self.to_json()

        return result

    def update_user(self):
        result = {}

        if self and self.id != 0:
            db.session.add(self)
            db.session.commit()
            result = self.to_json()

        return result

    def delete_user(self):
        result = {}

        if self and self.id != 0:
            db.session.delete(self)
            db.session.commit()
            result = self.to_json()

        return result

    # def generate_password(self):
    #     self.password = make_hashed("{}{}".format(self.password, self.salt))

    @classmethod
    def find_by_id(cls, user_id=0):
        result = cls()
        if user_id:
            result = db.session.query(cls) \
                         .filter(cls.id == user_id).first() or result

        return result

    @classmethod
    def find_by_email(cls, email):
        result = cls()

        if email:
            result = db.session.query(cls) \
                         .filter(cls.uid == email).first() or result

        return result
