from ..extensions import db
from datetime import time

class AgendaMedico(db.Model):
    __tablename__ = 'agendas_medicos'

    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    duracao_consulta = db.Column(db.Integer, default=30)
    ativo = db.Column(db.Boolean, default=True)

    medico = db.relationship('Medico', back_populates='agendas')
    agendamentos = db.relationship('Agendamento', back_populates='agenda', lazy=True)


    def __repr__(self):
        return f'<AgendaMedico {self.medico_id} - Day {self.data}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "medico_id": self.medico_id,
            "data": self.data,
            "hora_inicio": str(self.hora_inicio),
            "hora_fim": str(self.hora_fim)
        }