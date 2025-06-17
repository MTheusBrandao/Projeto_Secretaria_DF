from datetime import datetime
from ..models import Agendamento
from ..extensions import db
from ..services.horario_service import HorarioService

class AgendamentoService:
    @staticmethod
    def criar_agendamento(paciente_id, medico_id, data_hora, observacoes=None):
        
        disponivel, mensagem = HorarioService.verificar_disponibilidade(
            medico_id=medico_id,
            data_hora=data_hora
        )
    
        if not disponivel:
            return None, {'erro': mensagem}, 400
        
        agendamento = Agendamento(
            paciente_id=paciente_id,
            medico_id=medico_id,
            data_hora=data_hora,
            observacoes=observacoes
        )

        db.session.add(agendamento)
        db.session.commit()

        return agendamento, None, 201
    
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
        
        return agendamento, None, 200