from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status


SECRET_KEY = "4f1feeca525de4cdb064656007da3edac7895a87ff0ea865693300fb8b6e8f9c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINS = 30


def create_access_token(username: str, user_id: int, expires_in: timedelta or None = None): # type: ignore
    encode = {"sub": username, "id": user_id}
    expiration = datetime.now() + expires_in
    encode.update({"exp": expiration})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token, SECRET_KEY, algorithm=ALGORITHM):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[algorithm])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials.")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials.")