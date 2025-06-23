from datetime import datetime, timedelta
from flask import jsonify
from ..models import Agendamento, AgendaMedico, Medico
from ..extensions import db
from ..services.horario_service import HorarioService

class ServicoAgendamento:
    @staticmethod
    def criar_agendamento(paciente_id, agenda_id, data, horario):
        try:
            if not all([paciente_id, agenda_id, data, horario]):
                return None, {"erro": "Campos obrigatórios faltando"}, 400

            data_formatada = datetime.strptime(data, "%Y-%m-%d").date()
            horario_formatado = datetime.strptime(horario, "%H:%M:%S").time()

            agenda = AgendaMedico.query.get(agenda_id)
            if not agenda:
                return None, {"erro": "Agenda não encontrada"}, 404

            if not agenda.ativo:
                return None, {"erro": "Agenda está inativa"}, 400

            hora_fim_consulta = (datetime.combine(data_formatada, horario_formatado) + timedelta(minutes=agenda.duracao_consulta)).time()

            if not (agenda.hora_inicio <= horario_formatado < agenda.hora_fim):
                return None, {"erro": "Horário fora do intervalo da agenda"}, 400

            conflito = Agendamento.query.filter_by(
                agenda_id=agenda_id,
                data=data_formatada,
                horario=horario_formatado
            ).first()

            if conflito:
                return None, {"erro": "Horário já agendado"}, 409

            novo_agendamento = Agendamento(
                paciente_id=paciente_id,
                medico_id=agenda.medico_id,
                agenda_id=agenda_id,
                data=data_formatada,
                horario=horario_formatado
            )

            db.session.add(novo_agendamento)
            db.session.commit()

            return novo_agendamento.to_dict(), None, 201

        except Exception as e:
            db.session.rollback()
            print("❌ Erro em criar_agendamento:", e)  # <-- adicione isso
            return None, {"erro": f"Erro ao criar agendamento: {str(e)}"}, 500


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
        try:
            agendamento = Agendamento.query.get(agendamento_id)

            if not agendamento:
                return None, {'erro': 'Agendamento não encontrado'}, 404
            
            if agendamento.paciente_id != usuario_id:
                return None, {'erro': 'Não Autorizado'}, 403
            
            if agendamento.data < datetime.now().date():
                return None, {'erro': 'Não é possível cancelar agendamentos passados'}, 400
            
            agendamento.status = 'cancelado'
            db.session.commit()
            
            return agendamento.to_dict(), None, 200
        
        except Exception as e:
            db.session.rollback()
            return None, {'erro': f'Erro ao cancelar agendamento: {str(e)}'}, 500
