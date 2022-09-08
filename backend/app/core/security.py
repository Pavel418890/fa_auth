from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(
        claims=to_encode, key=settings.SECRET_KEY, algorithm=ALGORITHM
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_password_reset_token(email: str) -> str:
    expires = datetime.utcnow() + timedelta(
        hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS
    )
    to_encode = {"sub": email, "nbf": datetime.utcnow(), "exp": expires}
    return jwt.encode(
        claims=to_encode, key=settings.SECRET_KEY, algorithm=ALGORITHM
    )


def verify_access_token(token: str) -> Optional[dict[str, Any]]:
    try:
        token_data = jwt.decode(
            token=token, key=settings.SECRET_KEY, algorithms=ALGORITHM
        )
    except jwt.JWTError:
        return None
    else:
        return token_data


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_jwt = jwt.decode(
            token=token, key=settings.SECRET_KEY, algorithms=ALGORITHM
        )
        return decoded_jwt["email"]
    except jwt.JWTError:
        return None
