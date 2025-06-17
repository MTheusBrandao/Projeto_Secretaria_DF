from app import criar_aplicacao
from app.extensions import db, test_db_connection

app = criar_aplicacao()

with app.app_context():
    if not test_db_connection():
        print("❌ Falha na conexão com o banco de dados!")
    else:
        print("✅ Conexão com o banco de dados estabelecida!")

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)