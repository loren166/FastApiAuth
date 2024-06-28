import dotenv
import os
from authlib.jose import jwt
from datetime import timedelta, datetime
from fastapi import HTTPException

dotenv.load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_token(data: dict, live_time: timedelta = None):
    to_encode = data.copy()
    if live_time:
        expire = datetime.utcnow() + live_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    header = {'alg': ALGORITHM}
    to_encode.update({'exp': expire})
    token = jwt.encode(header, to_encode, SECRET_KEY.encode())
    return token.decode()


def verify_token(token: str):
    try:
        claims = jwt.decode(token.encode(), SECRET_KEY.encode())
        claims.validate()
        return claims
    except Exception:
        raise HTTPException(status_code=401, detail='Неверный токен')
