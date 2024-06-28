from datetime import timedelta
import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from psycopg2 import Error
from uuid import uuid4
from app.db import create_connection
from app.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_token
from app.models import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post('/register')
def register(user: User):
    connection = create_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail='Ошибка при подключении к бд')
    cursor = connection.cursor()
    try:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt=bcrypt.gensalt())
        user_id = uuid4()
        cursor.execute(
            "INSERT INTO users (id, name, password) VALUES (%s, %s, %s)",
            (str(user_id), user.name, hashed_password.decode('utf-8'))
        )
        connection.commit()
        return {**user.dict(), 'id': user_id}
    except (Exception, Error) as error:
        print('Ошибка при регистрации пользователя', error)
        raise HTTPException(status_code=500, detail='Ошибка при регистрации пользователя')
    finally:
        cursor.close()
        connection.close()


@router.post('/login')
def login(user: OAuth2PasswordRequestForm = Depends()):
    connection = create_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail='Ошибка при подключении к бд')
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT id, password FROM users WHERE name=%s",
            (user.username,)
        )
        stored_password = cursor.fetchone()
        if stored_password is None or not bcrypt.checkpw(user.password.encode('utf-8'), stored_password[1].encode('utf-8')):
            raise HTTPException(status_code=400, detail='Неверные данные')
        user_id = stored_password[0]
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_token(data={"sub": str(user_id)}, live_time=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    except (Exception, Error) as error:
        print('Ошибка при логине', error)
    finally:
        cursor.close()
        connection.close()
