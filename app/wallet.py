import hashlib
import uuid
from config import GetEnvData
from db.database import CreateConnection

env_data = GetEnvData()

def GenerateWallet(user_id):
    wallet_id = str(uuid.uuid4())
    public_key = hashlib.sha256(wallet_id.encode()).hexdigest()
    private_key = hashlib.sha256((wallet_id + env_data['SECRET_KEY']).encode()).hexdigest()
    
    # Salva a carteira no banco de dados
    connection = CreateConnection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO wallets (user_id, public_key, private_key, balance)
        VALUES (%s, %s, %s, %s)
    ''', (user_id, public_key, private_key, 0))
    connection.commit()
    cursor.close()
    connection.close()
    return {"wallet_id": wallet_id, "public_key": public_key, "private_key": private_key}

def GetWalletBalance(public_key):
    connection = CreateConnection()
    cursor = connection.cursor()
    cursor.execute('SELECT balance FROM wallets WHERE public_key = %s', (public_key,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result else 0
