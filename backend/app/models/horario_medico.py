from ..extensions import db
from datetime import time

class HorarioMedico(db.Model):
    __tablename__ = 'horarios_medicos'

    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    dia_semana = db.Column(db.Integer, nullable=False)  # 0=Segunda, 6=Domingo
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    medico = db.relationship('Medico', backref='horarios')

    def to_dict(self):
        return{
            'id': self.id,
            'dia_semana': self.dia_semana,
            'hora_inicio': self.hora_inicio,
            'hora_fim': self.hora_fim.isoformat(),
            'ativo': self.ativo
        }