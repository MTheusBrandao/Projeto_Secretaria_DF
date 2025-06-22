from flask import Flask
from .config import Config
from .extensions import db, jwt, migrate
from dotenv import load_dotenv
from sqlalchemy import text


load_dotenv()

def criar_aplicacao(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # inicializar as extensoes:
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Testar conexão com o banco de dados
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            print("Conexão com o banco de dados bem-sucedida!")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    from .routes.autenticacao_routes import bp as auth_bp
    from .routes.medico_routes import bp as medico_bp
    from .routes.agendamento_routes import bp as agendamento_bp
    from .routes.horario_routes import bp as horario_bp
    from .routes.administracao_routes import bp as admin_bp


    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(medico_bp, url_prefix="/api/medicos")
    app.register_blueprint(agendamento_bp, url_prefix="/api/agendamentos")
    app.register_blueprint(horario_bp, url_prefix="/api/horarios")



    return app