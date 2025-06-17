from ..extensions import db

class Especialidade(db.Model):
    __tablename__= 'especialidades'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(10), unique=True, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=True)

    medicos = db.relationship('Medico', back_populates='especialidade')
