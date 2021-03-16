# Created security.py by KimDaeil on 04/26/2018
from datetime import datetime
from base64 import b64encode, b64decode
from hashlib import sha3_256
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):

    def __init__(self, key=None, iv=None):
        self.bs = 32
        if key is None:
            from flask import current_app
            key = current_app.config.get("SECRET_KEY")

        self.key = b64encode(sha3_256(key.encode()).digest()).decode("utf-8")[:AES.block_size]
        self.iv = iv[:AES.block_size] if iv and isinstance(iv, bytes) and len(iv) >= AES.block_size else Random.new().read(AES.block_size)
        # print("{{password}} AESCipher.iv >>", self.iv)
        # if not iv or not isinstance(iv, str) or len(iv) < AES.block_size:
        #     self.iv = Random.new().read(AES.block_size)
        # else:
        #     self.iv = iv

    def encrypt(self, raw):
        result = ""

        try:
            raw = self._pad(raw)
            cipher = AES.new(self.key, mode=AES.MODE_CBC, IV=self.iv)
            result = b64encode(self.iv + cipher.encrypt(raw)).decode('utf-8')
        except Exception as e:
            print("AESCipher.decrypt >> ", e)

        return result

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def decrypt(self, enc):
        result = ""

        try:
            enc = b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, mode=AES.MODE_CBC, IV=iv)
            result = self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
        except Exception as e:
            print("AESCipher.decrypt >> ", e)

        return result

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


def make_hashed(data):
    if data:
        if not isinstance(data, str):
            data = str(data)

        data = data.encode()

        print(__name__, "make_hashed data >> ", data)
        return b64encode(sha3_256(data).digest()).decode('utf-8')

    return None


def make_session_salt(salt):
    return make_hashed("{}{}".format(salt, datetime.now()))


def generate_salt():
    import random
    import string

    return ''.join(random.choice(string.lowercase) for _ in range(32))

# def generate_password(user):
#     if user and isinstance(user, UserModel):
#         user.salt = make_hashed(datetime.now())
#         user.password = make_hashed("{}{}".format(user.password, user.salt))


# def make_password_hash(password, salt):
#     hashed_password = ""
#
#     if password and salt:
#         if not isinstance(password, str):
#             password = str(password)
#
#         if not isinstance(salt, str):
#             salt = str(salt)
#
#         hashed_password = make_hashed("{}{}".format(password, salt))
#
#     return hashed_password
#
