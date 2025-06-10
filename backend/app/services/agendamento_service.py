from datetime import datetime, timedelta
from ..models import Agendamento, Medico, Usuario
from ..extensions import db

class AgendamentoService:
    @staticmethod
    def criar_agendamento(paciente_id, medico_id, data_hora, observacoes=None):
        # verificar conflitos de horario
        fim_consulta = data_hora + timedelta(minutes=30)

        conflito = Agendamento.query.filter(
            Agendamento.medico_id == medico_id,
            Agendamento.data_hora < fim_consulta,
            Agendamento.data_hora + timedelta(minutes=Agendamento.duracao) > data_hora,
            Agendamento.status == 'agendado'
        ).first()

        if conflito:
            return None, {'erro': 'Já existe outro agendamento nesse horario'}, 409
        
        agendamento = Agendamento(
            paciente_id=paciente_id,
            medico_id=medico_id,
            data_hora=data_hora,
            observacoes=observacoes
        )

        db.session.add(agendamento)
        db.session.commit()

        return agendamento, None
    
    @staticmethod
    def listar_agendamentos(medico_id=None, paciente_id=None):
        query = Agendamento.query

        if medico_id:
            query = query.filter_by(medico_id=medico_id)
        if paciente_id:
            query = query.filter_by(paciente_id=paciente_id)
        
        return query.order_by(Agendamento.data_hora).all()

    @staticmethod
    def cancelar_agendamento(agendamento_id, usuario_id):
        agendamento = Agendamento.query.get(agendamento_id)

        if not agendamento:
            return None, {'erro': 'Agendamento não encontrado'}, 404
        
        if agendamento.paciente_id != usuario_id:
            return None, {'erro': 'Não Autorizado'}, 403
        
        if agendamento.data_hora < datetime.now():
            return None, {'erro': 'Não é possível cancelar agendamentos passados'}, 400
        
        agendamento.status = 'cancelado'
        db.session.commit()
        
        return agendamento, None