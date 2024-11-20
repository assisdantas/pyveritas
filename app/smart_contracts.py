class SmartContract:
    def __init__(self, contract_id, creator, code, state=None):
        self.contract_id = contract_id
        self.creator = creator
        self.code = code  # Código do contrato em Python
        self.state = state or {}

    def Execute(self, **kwargs):
        try:
            exec(self.code, None, kwargs)
            return kwargs.get('output', None)
        except Exception as e:
            return {"error": str(e)}

# Exemplo de contrato
sample_contract = SmartContract(
    contract_id="contract1",
    creator="public_key_of_creator",
    code="""

"""
)

# Executando o contrato
result = sample_contract.Execute(arg1=10, arg2=20)
print(result)  # Output: 30
