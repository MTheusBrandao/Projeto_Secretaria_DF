from datetime import datetime
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=True)
    telefone = db.Column(db.String(15), nullable=True)
    endereco = db.Column(db.Text, nullable=True)
    tipo = db.Column(db.String(20), nullable=False, default='paciente')
    criado_em = db.Column(db.DateTime, default=datetime.now)
    ativo = db.Column(db.Boolean, default=True)

    agendamentos = db.relationship('Agendamento', back_populates='paciente', lazy='dynamic')


    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(
            senha,
            method='pbkdf2:sha256',
            salt_length=8
        )

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'tipo': self.tipo,
        }