from ..extensions import db
from datetime import datetime, time

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'

    id = db.Column(db.Integer, primary_key=True)
    
    # Chaves estrangeiras necessárias
    paciente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    agenda_id = db.Column(db.Integer, db.ForeignKey('agendas_medicos.id'), nullable=False)

    data = db.Column(db.Date, nullable=False)
    horario = db.Column(db.Time, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    paciente = db.relationship('Usuario', back_populates='agendamentos')
    medico = db.relationship('Medico', back_populates='agendamentos')
    agenda = db.relationship('AgendaMedico', back_populates='agendamentos')

    def __repr__(self):
        return f'<Agendamento {self.id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "paciente_id": self.paciente_id,
            "medico_id": self.medico_id,
            "agenda_id": self.agenda_id,
            "data": self.data.isoformat(),
            "horario": self.horario.strftime('%H:%M:%S'),
            "criado_em": self.criado_em.isoformat()
        }
