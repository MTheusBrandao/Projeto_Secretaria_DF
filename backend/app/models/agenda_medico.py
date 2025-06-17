from ..extensions import db
from datetime import time

class AgendaMedico(db.Model):
    __tablename__ = 'agendas_medicos'

    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    dia_semana = db.Column(db.Integer, nullable=False)  # 0=Segunda, 6=Domingo
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    duracao_consulta = db.Column(db.Integer, default=30)
    ativo = db.Column(db.Boolean, default=True)
