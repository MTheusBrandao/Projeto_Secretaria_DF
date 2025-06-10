from app import criar_aplicacao
from app.extensions import db

app = criar_aplicacao()

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()
    print("Banco de dados iniciado!")

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)