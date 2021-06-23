from functools import wraps
from graphql import GraphQLError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
import jwt


def valid_auth():
    def decorator_auth(func):
        @wraps(func)
        def wrapper(any, info, *args, **kwargs):
            auth = info.context["request"].headers.get('Authorization', None)
            if not auth:
                raise GraphQLError('Auth is required for this service')
            header, token = auth.split()
            try:
                payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms="HS256")
                if payload['is_active']:
                    info.context['user'] = payload
                    return func(any, info,  *args, **kwargs)
                else:
                    raise GraphQLError('User inactive')
            except Exception as e:
                raise GraphQLError('Invalid Token')
        return wrapper
    return decorator_auth


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_jwt_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=90)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms="HS256")
        if payload.sub is not None:
            return payload
        return None
    except Exception:
        return None


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hash_password: str):
    return pwd_context.verify(password, hash_password)