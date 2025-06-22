from datetime import datetime
from ..extensions import db

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    duracao = db.Column(db.Integer, default=30)  # em minutos
    status = db.Column(db.String(20), default='agendado')  # agendado, cancelado, realizado
    observacoes = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    paciente = db.relationship('Usuario', back_populates='agendamentos')
    medico = db.relationship('Medico', back_populates='agendamento')

    # LGPD
    consentimento = db.Column(db.Boolean, default=False)
    finalidade_dados = db.Column(db.String(200), default='Agendamento de consulta médica')

    def __repr__(self):
        return f'<Appointment {self.id} - {self.data_hora}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "paciente_id": self.paciente_id,
            "medico_id": self.medico_id,
            "data_hora": self.data_hora.isoformat(),
            "status": self.status
        }
