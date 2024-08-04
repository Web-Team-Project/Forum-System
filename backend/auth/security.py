from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password, hashed_password):
    return password_context.verify(password, hashed_password)


def get_password_hash(password):
    return password_context.hash(password)
