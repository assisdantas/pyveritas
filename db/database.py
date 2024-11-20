import psycopg2
from app.block import Block
from config import GetEnvData
from pymongo import MongoClient
from config import GetEnvData

env_data = GetEnvData()
client = MongoClient(env_data['MONGO_URI'])
db = client[env_data['MONGO_DB_NAME']]

DB_NAME = env_data['DB_NAME']
DB_USER = env_data['DB_USER']
DB_PASSWORD = env_data['DB_PASSWORD']
DB_HOST = env_data['DB_HOST']
DB_PORT = env_data['DB_PORT']

def SaveBlockToDB(block):
    db.blocks.insert_one(block.ToDict())

def LoadBlockchain():
    return [Block.FromDict(b) for b in db.blocks.find()]

def CreateConnection():
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return connection

def CreateDatabase():
    connection = CreateConnection()
    cursor = connection.cursor()
    
    cursor.execute('''
CREATE TABLE IF NOT EXISTS blocks (
    index SERIAL PRIMARY KEY,
    previous_hash TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    transactions TEXT NOT NULL,
    hash TEXT NOT NULL,
    nonce INTEGER NOT NULL
);
''')
    
    cursor.execute('''
CREATE TABLE auth_tokens (
    id SERIAL PRIMARY KEY,
    node_id INTEGER NOT NULL,
    token TEXT NOT NULL,
    expiration TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')
    
    cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL
);                   
''')
    
    connection.commit()
    cursor.close()
    connection.close()

def SaveBlockToDB(block):
    connection = CreateConnection()
    cursor = connection.cursor()
    
    cursor.execute('''
INSERT INTO blocks (previous_hash, timestamp, transactions, hash, nonce)
VALUES (%s, %s, %s, %s, %s)
''', (block.previous_hash, block.timestamp, str(block.transactions), block.hash, block.nonce))
    
    connection.commit()
    cursor.close()
    connection.close()

def LoadBlockFromDB():
    connection = CreateConnection()
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM blocks ORDER BY index')
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    # Reconstruir a blockchain a partir dos registros do banco de dados
    return [Block(*rows) for row in rows]