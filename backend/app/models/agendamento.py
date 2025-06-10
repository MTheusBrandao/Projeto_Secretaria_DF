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
    criado_em = db.Column(db.DateTime, default=datetime.now)

    paciente = db.relationship('Usuario', backref='agendamentos')
    medico = db.relationship('Medico', backref='agendamentos')

    def to_dict(self):
        return {
            'id': self.id,
            'data_hora': self.data_hora.isoformat(),
            'duracao': self.duracao,
            'status': self.status,
            'medico': self.medico.to_dict(),
            'paciente': {
                'id':self.paciente.id,
                'nome': self.paciente.nome
            },
            'observacoes': self.observacoes
        }