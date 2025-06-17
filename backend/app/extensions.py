from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy import text

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def test_db_connection():
    try:
        db.session.execute(text('SELECT 1'))
        db.session.commit()  
        print("✅ Conexão com o banco de dados verificada!")
        return True
    except Exception as e:
        db.session.rollback()  
        print(f"❌ Erro na conexão com o banco: {str(e)}")
        return False