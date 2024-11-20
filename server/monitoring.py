from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from db.database import CreateConnection

app = Flask(__name__)
admin = Admin(app, name='Blockchain Monitoring', template_mode='bootstrap3')

# Adicione visualizações ao Flask-Admin
connection = CreateConnection()

class BlockModelView(ModelView):
    pass

class WalletModelView(ModelView):
    pass

admin.add_view(BlockModelView(connection.blocks, name="Blocks"))
admin.add_view(WalletModelView(connection.wallets, name="Wallets"))
