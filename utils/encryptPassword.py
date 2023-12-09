import os
from argon2 import PasswordHasher, hash_password, verify_password, Type

# from Crypto.Hash import SHA512

ph = PasswordHasher(type=Type.ID, memory_cost=2**16, hash_len=50)

# def encryptPasswordOld(password):
#     encryptedHex = SHA512(password).toString()

#     return encryptedHex


def encryptPassword(password):
    # password_encrypted = hash_password(
    #     password,
    #     type=Type.ID,
    #     memory_cost=2**16,
    #     hash_len=50,
    #     # salt=bytes.fromhex(str(os.getenv("APP_TOKEN_SECRET"))),
    # )

    password_encrypted = ph.hash(
        password,
        # salt=bytes.fromhex(str(os.getenv("APP_TOKEN_SECRET"))),
    )

    return password_encrypted


def verifyPassword(password, userEnter):
    # salt = {str(os.getenv("APP_TOKEN_SECRET")).encode("utf-8")}

    return ph.verify(password, f"{userEnter}")
