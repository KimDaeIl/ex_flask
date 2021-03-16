# Created sessions.py by KimDaeil on 04/25/2018

from core.models.mongos import mongo


class SessionMongo:
    @classmethod
    def create_session(cls, session):

        print("create_session >> ", session)
        if session and isinstance(session, dict):
            if "id" in session and isinstance(session["id"], int):
                print("mongos.SessionMongo.create >> ",
                      mongo.db.session.update_one({"id": session["id"]}, {'$set': session}, upsert=True))

        return session

    @classmethod
    def delete_session(cls, session):
        if session and isinstance(session, dict):
            if "id" in session and isinstance(session["id"], int):
                print("mongos.SessionMongo.delete >> ", mongo.db.session.delete_one(session))

    @classmethod
    def find_by_id(cls, user_id):
        result = {}
        if user_id and isinstance(user_id, int):
            data = mongo.db.session.find_one({"id": user_id}, {"_id": False})

            if data:
                result = data

        print("mongos.SessionMongo.find_by_id >> ", result)

        return result

    @classmethod
    def find_by_session(cls, arg):

        session = {}
        if arg and len(arg) > 0:
            temp = mongo.db.session.find_one({"session": arg}, {"_id": False})

            if temp:
                session = temp

        return session
