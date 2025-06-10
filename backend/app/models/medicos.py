from datetime import datetime
from ..extensions import db

class Medico(db.Model):
    __tablename__ = 'medicos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    crm = db.Column(db.String(20), unique=True, nullable=False)
    especialidade_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    especialidade = db.relationship('Especialidade', backref='medicos')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'crm': self.crm,
            'especialidade': self.especialidade.to_dict() if self.especialidade else None,
            'ativo': self.ativo
        }