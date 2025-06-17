from datetime import datetime
from ..extensions import db

class Medico(db.Model):
    __tablename__ = 'medicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    crm = db.Column(db.String(20), unique=True, nullable=False)
    especialidade_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'), nullable=False)
    regiao_administrativa_id = db.Column(db.Integer, db.ForeignKey('admins_regionais.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    
    consultas = db.relationship('Consulta', backref='medico', lazy=True)
    agendas = db.relationship('AgendaMedico', backref='medico', lazy=True)