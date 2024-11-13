import jwt 
import bcrypt
from flask import request, jsonify
from flask_httpauth import HTTPTokenAuth 
from config import GetEnvData
from db.database import CreateConnection

env_data = GetEnvData()
SECRET_KEY = env_data['SECRET_KEY']

auth = HTTPTokenAuth(scheme='Bearer')

def RegisterUser(username, password):
    connection = CreateConnection()
    cursor = connection.cursor()

    cursor.execute('''
SELECT user_id FROM users WHERE username = %s
''', (username,))
    
    user = cursor.fetchone()

    if user:
        cursor.close()
        connection.close()
        return None
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    cursor.execute('''
INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id
''', (username, hashed_password))
    user_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return user_id

def LoginUser(username, password):
    connection = CreateConnection()
    cursor = connection.cursor()

    cursor.execute('''
SELECT id, password FROM users WHERE username = %s
''', (username,))
    
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user:
        return None
    
    stored_password = user[1]

    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')): 
        token = GenerateToken(user[0])
        return token
    return None

def SaveTokenToDB(node_id, token, expiration_time):
    connection = CreateConnection()
    cursor = connection.cursor()
    
    cursor.execute('''
       INSERT INTO auth_tokens (node_id, token, expiration)
       VALUES (%s, %s, %s)
    ''', (node_id, token, expiration_time))

    connection.commit()
    cursor.close()
    connection.close()

def GenerateToken(node_id):
    import datetime
    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    payload = {'node_id': node_id, 'exp':expiration_time}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    SaveTokenToDB(node_id, token, expiration_time)
    return token

@auth.VerifyTokenFromDB
def VerifyTokenFromDB(token):
    connection = CreateConnection()
    cursor = connection.cursor()

    cursor.execute('''
SELECT * FROM auth_tokens WHERE token = %s
''', (token,))
    
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if not result:
        return False

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        node_id = payload.get('node_id')
        if node_id is None:
            return False

        return node_id == result[1]

    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    
@auth.RevokeTokenFromDB
def RevokeTokenFromDB(token):
    connection = CreateConnection()
    cursor = connection.cursor()

    cursor.execute('''
DELETE FROM auth_tokens WHERE token = %s
''', (token,))
    
    connection.commit()
    cursor.close()
    connection.close()