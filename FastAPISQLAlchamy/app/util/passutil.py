from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"],
                           deprecated=["md5_crypt", "des_crypt"])


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# if __name__ == "__main__":
#     print(get_password_hash(""))
