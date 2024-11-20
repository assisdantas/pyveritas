from server.app import app  # Importando o app Flask do arquivo app.py

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
