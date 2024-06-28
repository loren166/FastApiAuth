import os
import dotenv
import psycopg2
from psycopg2 import Error

dotenv.load_dotenv()


def create_connection():
    try:
        dbconnection = psycopg2.connect(user=os.getenv("DBUSER"),
                                        password=os.getenv("DBPASSWORD"),
                                        host=os.getenv("DBHOST"),
                                        port=os.getenv("DBPORT"),
                                        database=os.getenv("DB"))
        return dbconnection
    except (Exception, Error) as error:
        print('Ошибка при работе с бд', error)
        return None


def create_table(dbconnection):
    cursor = None
    try:
        cursor = dbconnection.cursor()
        create_table_query = '''CREATE TABLE IF NOT EXISTS users (
                                    id UUID PRIMARY KEY,
                                    name VARCHAR(50) NOT NULL,
                                    password VARCHAR(400) NOT NULL
                                );'''
        cursor.execute(create_table_query)
        dbconnection.commit()
        print('Таблица Users успешно создана')
    except (Exception, Error) as error:
        print('Ошибка при создании таблицы', error)
    finally:
        if cursor:
            cursor.close()


dbconnection = create_connection()
if dbconnection:
    create_table(dbconnection)
    dbconnection.close()
