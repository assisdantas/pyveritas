import os
from dotenv import load_dotenv

load_dotenv()

def GetEnvData():
    DB_NAME = os.getenv['DB_NAME'],
    DB_USER = os.getenv['DB_USER'],
    DB_PASSWORD = os.getenv['DB_PASSWORD'],
    DB_HOST = os.getenv['DB_HOST'],
    DB_PORT = os.getenv['DB_PORT']
    SECRET_KEY = os.getenv['SECRET_KEY']
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

    return {
        'DB_NAME': DB_NAME,
        'DB_USER': DB_USER,
        'DB_PASSWORD': DB_PASSWORD,
        'DB_HOST': DB_HOST,
        'DB_PORT': DB_PORT,
        'SECRET_KEY': SECRET_KEY,   
        'MONGO_URI': MONGO_URI,
        'MONGO_DB_NAME': MONGO_DB_NAME
    }
