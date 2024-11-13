from flask import Flask, jsonify, request
from flask_httpauth import HTTPTokenAuth
from app.blockchain import Blockchain
from db.database import SaveBlockToDB, LoadBlockFromDB
from .auth import auth, LoginUser, RegisterUser
import requests

app = Flask(__name__)
blockhain = Blockchain()
auth = HTTPTokenAuth(scheme='Bearer')

@app.route('/register', methods=['POST'])
def RegisterRoute():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user_id = RegisterUser(username, password)
    
    if user_id:
        return jsonify({'message': 'User registered successfully.'}), 201
    else:
        return jsonify({'message': 'Username already exists'}), 400

@app.route('/login', methods=['POST'])
def LoginRoute():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Chama a função de login
    token = LoginUser(username, password)
    
    if token:
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/mine_block', methods=['POST'])
@auth.login_required
def MineBlock():
    transactions = request.json.get('transactions')
    if not transactions:
        return jsonify({"message": "No transaction provided"}), 400
    new_block = blockhain.AddBlock(transactions)
    SaveBlockToDB(new_block)
    return jsonify({"message":"Block mined successfully.", "block": new_block.index}), 201

@app.route('/get_chain', methods=['GET'])
def GetChain():
    chain_data = LoadBlockFromDB()
    return jsonify(chain_data), 200

if __name__ == '__main__':
    #app.run(ssl_context=('cert.pem', 'key.pem')), port=5000
    app.run(port=5000)