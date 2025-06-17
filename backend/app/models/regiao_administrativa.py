from ..extensions import db

class RegiaoAdministrativa(db.Model):
    __tablename__ = 'regioes_administrativas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(10), unique=True, nullable=False)
    endereco = db.Column(db.Text, nullable=True)
    telefone = db.Column(db.String(15), nullable=True)
    ativo = db.Column(db.Boolean, default=True)

    medicos = db.relationship('Medico', back_populates='regiao_administrativa', lazy=True)