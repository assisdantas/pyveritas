from flask import Flask, jsonify, request
from flask_httpauth import HTTPTokenAuth
from app.blockchain import Blockchain
from app.block import Block
from app.wallet import GetWalletBalance, GenerateWallet
from db.database import SaveBlockToDB, LoadBlockFromDB
from .auth import auth, LoginUser, RegisterUser, GenerateNodeId
import requests
import uuid
from db.database import CreateConnection

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
        node_id, mnemonic = GenerateNodeId()
        return jsonify({"token": token,
                        "node_id": node_id,
                        "mnemonic": mnemonic}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
@app.route('/sync_chain', methods=['GET'])
def SyncChain():
    return jsonify([block.ToDict() for block in Blockchain.chain]), 200

@app.route('/mine_block', methods=['POST'])
@auth.login_required
def MineBlock():
    transactions = request.json.get('transactions')
    if not transactions:
        return jsonify({"message": "No transaction provided"}), 400
    new_block = blockhain.AddBlock(transactions)
    SaveBlockToDB(new_block)
    return jsonify({"message":"Block mined successfully.", "block": new_block.index}), 201

@app.route('/get_block_to_mine', methods=['GET'])
@auth.login_required
def GetBlockToMine():
    transactions = Blockchain.GetPendingTransactions()
    previous_block = Blockchain.GetLasBlock()
    return jsonify({
        "index": previous_block.index + 1,
        "previous_hash": previous_block.hash,
        "transactions": transactions
    }), 200

@app.route('/create_wallet', methods=['POST'])
@auth.login_required
def CreateWallet():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400
    wallet = GenerateWallet(user_id)
    return jsonify(wallet), 201

@app.route('/get_balance/<public_key>', methods=['GET'])
def GetBalance(public_key):
    balance = GetWalletBalance(public_key)
    return jsonify({"balance": balance}), 200

@app.route('/submit_mined_block', methods=['POST'])
@auth.login_required
def SubmitMinedBlock():
    data = request.json
    index = data.get('index')
    previous_hash = data.get('previous_hash')
    transactions = data.get('transactions')
    nonce = data.get('nonce')

    is_valid = Blockchain.ValidadeBlock(index, previous_hash, transactions, nonce)
    if not is_valid:
        return jsonify({
            "message":"Invalid block"
        }), 400
    
    new_block = Blockchain.AddBlock(transactions, nonce)
    Blockchain.NotifyNodes(new_block)

    return jsonify({
        "message":"Block added to the blockchain."
    }), 201

@app.route('/submit_block', methods=['POST'])
@auth.login_required
def SubmitBlock():
    data = request.json
    node_id = auth.current_user()
    block_data = data.get('block')
    
    if not block_data:
        return jsonify({"message": "Block data is required."}), 400
    
    block = Block.FromDict(block_data)
    if not Blockchain.ValidateBlock(block):
        Blockchain.PenalizeNode(node_id, penalty_amount=10)  # Penalidade de 10 stakes
        return jsonify({"message": "Invalid block. You have been penalized."}), 400
    
    Blockchain.chain.append(block)
    SaveBlockToDB(block)
    return jsonify({"message": "Block accepted and added to the chain."}), 201

@app.route('/add_stake', methods=['POST'])
@auth.login_required
def AddStake():
    data = request.json
    node_id = data.get('node_id')
    stake = data.get('stake')
    if not node_id or not stake:
        return jsonify({"message": "Node ID and stake are required."}), 400

    Blockchain.AddStake(node_id, stake)
    return jsonify({"message": "Stake added successfully."}), 201

@app.route('/get_block_to_validate', methods=['GET'])
@auth.login_required
def GetBlockToValidate():
    try:
        validator = Blockchain.SelectValidator()
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    if validator != auth.current_user():
        return jsonify({"message": "You are not the selected validator."}), 403

    previous_block = Blockchain.GetLastBlock()
    return jsonify({
        "index": previous_block.index + 1,
        "previous_hash": previous_block.hash,
        "transactions": Blockchain.pending_transactions
    }), 200

@app.route('/update_chain', methods=['POST'])
@auth.login_required
def UpdateChain():
    data = request.json
    incoming_chain = [Block.FromDict(b) for b in data.get('chain', [])]

    if not Blockchain.ValidateChain(incoming_chain):
        return jsonify({"message": "Invalid blockchain received."}), 400

    Blockchain.chain = incoming_chain
    return jsonify({"message": "Blockchain updated successfully."}), 200

@app.route('/validate_block', methods=['POST'])
@auth.login_required
def ValidateBlockDistributed():
    data = request.json
    block_data = data.get('block')
    validators = data.get('validators') 
    
    if not block_data or not validators:
        return jsonify({"message": "Block data and validators are required."}), 400

    block = Block.FromDict(block_data)
    is_valid = Blockchain.ValidateBlockDistributed(block, validators)
    
    if is_valid:
        Blockchain.chain.append(block)
        SaveBlockToDB(block)
        return jsonify({"message": "Block accepted by majority vote."}), 201
    else:
        return jsonify({"message": "Block rejected by majority vote."}), 400
    
@app.route('/create_contract', methods=['POST'])
@auth.login_required
def CreateContract():
    data = request.json
    creator = data.get('creator')
    code = data.get('code')
    if not creator or not code:
        return jsonify({"message": "Creator and code are required"}), 400
    contract_id = str(uuid.uuid4())

    # Salvar contrato no banco
    connection = CreateConnection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO smart_contracts (creator, code)
        VALUES (%s, %s)
    ''', (creator, code))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({"contract_id": contract_id}), 201

@app.route('/get_chain', methods=['GET'])
def GetChain():
    chain_data = LoadBlockFromDB()
    return jsonify(chain_data), 200

if __name__ == '__main__':
    #app.run(ssl_context=('cert.pem', 'key.pem')), port=5000
    app.run(port=5000)