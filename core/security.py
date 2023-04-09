from passlib.context import CryptContext
from core.config import HASH_SALT

import secrets
import string
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def bcrypt_password(password):
    return pwd_cxt.hash(password + HASH_SALT)


def verify_password(plain_password, hashed_password):
    return pwd_cxt.verify(plain_password + HASH_SALT, hashed_password)


def generate_user_code():
    alphabet = string.digits + string.ascii_letters
    code = ''.join(secrets.choice(alphabet) for i in range(7))
    return code
