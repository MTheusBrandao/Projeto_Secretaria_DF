from ..extensions import db

class Medico(db.Model):
    __tablename__ = 'medicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    crm = db.Column(db.String(20), unique=True, nullable=False)
    especialidade_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'), nullable=False)
    regiao_administrativa_id = db.Column(db.Integer, db.ForeignKey('regioes_administrativas.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    
    agendamento = db.relationship('Agendamento', back_populates='medico', lazy=True)
    agendas = db.relationship('AgendaMedico', back_populates='medico', lazy=True)
    especialidade = db.relationship('Especialidade', back_populates='medicos')
    regiao_administrativa = db.relationship('RegiaoAdministrativa', back_populates='medicos')



    def __repr__(self):
        return f'<Medico {self.nome}>'