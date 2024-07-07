from datetime import timedelta, datetime
import os
from jwt import (
    JWT,
    jwk_from_pem,
)
from typing import Dict
from pathlib import Path
from jwt.utils import get_int_from_datetime
from app.conf import EmailSettings


def get_root() -> str:
    return str(Path(__file__).parent.parent) + os.sep


class AccessToken:
    """ Access Token Util Class"""

    def __init__(self):

        self.__instance = JWT()
        self.__algorithm = "RS256"
        with open(get_root() + 'auth' + os.sep + 'jwtRS256_private.pem',
                  'rb') as fh:
            self.__signing_key = jwk_from_pem(fh.read())
        with open(get_root() + 'auth' + os.sep + 'jwtRS256_public.pem',
                  'rb') as fh:
            self.__verifying_key = jwk_from_pem(fh.read())

    def create_access_token(self, *, data: dict,
                            expires_delta: timedelta = None) -> str:
        """Create Access Token Using JWT with RSA256 Encryption"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"ist": get_int_from_datetime(datetime.utcnow())})
        to_encode.update({"exp": get_int_from_datetime(expire)})
        encoded_jwt = self.__instance.encode(to_encode, self.__signing_key,
                                             self.__algorithm)
        return encoded_jwt

    def decode_access_token(self, *, token: str) -> Dict:
        """ Decode Access Token """
        return self.__instance.decode(token, self.__verifying_key,
                                      do_time_check=False)

    def generate_password_reset_token(self, email: str) -> str:
        """ Generate Access Token for password Reset email"""
        delta = timedelta(hours=EmailSettings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
        now = datetime.utcnow()
        expires = now + delta
        encoded_jwt = self.__instance.encode(
            {"exp": get_int_from_datetime(expires),
             "ist": get_int_from_datetime(now), "sub": email},
            self.__signing_key,
            alg=self.__algorithm,
        )
        return encoded_jwt

    def verify_password_reset_token(self, token: str) -> Dict:
        """ Decode Access Token """
        return self.__instance.decode(token, self.__verifying_key,
                                      do_time_check=False)


access_token = AccessToken()
