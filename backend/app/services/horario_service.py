from datetime import time, timedelta, datetime
from ..models import AgendaMedico, Medico, Agendamento
from ..extensions import db

class HorarioService:
    @staticmethod
    def cadastrar_horario(medico_id, dia_semana, hora_inicio, hora_fim):
        if not Medico.query.get(medico_id):
            return None, {'erro': 'Medico não encontrado'}, 404
        
        try:
            hora_inicio = time.fromisoformat(hora_inicio) if isinstance(hora_inicio, str) else hora_inicio
            hora_fim = time.fromisoformat(hora_fim) if isinstance(hora_fim, str) else hora_fim
        except ValueError:
            return None, {'erro': 'Formato de hora invalido'}, 404

        horario = AgendaMedico(
            medico_id=medico_id,
            dia_semana=dia_semana,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )

        db.session.add(horario)
        db.session.commit()
        
        return horario, None
    
    @staticmethod
    def listar_horarios(medico_id, apenas_ativos=True):
        query = AgendaMedico.query.filter_by(medico_id=medico_id)

        if apenas_ativos:
            query = query.filter_by(ativo=True)

        return query.order_by(AgendaMedico.dia_semana, AgendaMedico.hora_inicio).all()
    
    @staticmethod
    def verificar_disponibilidade(medico_id, data, duracao_minutos=30):
       
        try:
            if isinstance(data_hora, str):
                data_hora = datetime.fromisoformat(data_hora)
                
            dia_semana = data_hora.weekday()
            hora_consulta = data_hora.time()
            fim_consulta = (data_hora + timedelta(minutes=duracao_minutos)).time()
            
            horario = AgendaMedico.query.filter_by(
                medico_id=medico_id,
                dia_semana=dia_semana,
                ativo=True
            ).filter(
                AgendaMedico.hora_inicio <= hora,
                AgendaMedico.hora_fim >= fim
            ).first()
            
            if not horario:
                return False, "Médico não atende neste horário"
                
            conflito = Agendamento.query.filter_by(
                medico_id=medico_id,
                status='agendado'
            ).filter(
                Agendamento.data_hora < data_hora + timedelta(minutes=duracao),
                Agendamento.data_hora + timedelta(minutes=Agendamento.duracao) > data_hora
            ).first()
            
            if conflito:
                return False, "Horário já agendado"
                
            # 3. Verificar se não é no passado
            if data_hora < datetime.now():
                return False, "Não é possível agendar no passado"
                
            return True, "Horário disponível"
            
        except Exception as e:
            return None, str(e)

    @staticmethod
    def listar_horarios_disponiveis(medico_id, data):
        
        try:
            if isinstance(data, str):
                data = datetime.strptime(data, '%Y-%m-%d').date()
                
            dia_semana = data.weekday()
            data_atual = datetime.now().date()
            
            horarios = AgendaMedico.query.filter_by(
                medico_id=medico_id,
                dia_semana=dia_semana,
                ativo=True
            ).order_by(AgendaMedico.horario_inicio).all()
            
            if not horarios:
                return []
                
            inicio = datetime.combine(data, time.min)
            fim = datetime.combine(data, time.max)

            agendados = Agendamento.query.filter_by(
                medico_id=medico_id,
                status='agendado'
            ).filter(Agendamento.data_hora.between(inicio, fim)).all()

            disponiveis = []
            for horario in horarios:
                atual = datetime.combine(data, horario.horario_inicio)
                limite = datetime.combine(data, horario.horario_fim)

                while atual + timedelta(minutes=30) <= limite:
                    conflito = any(
                        not (atual + timedelta(minutes=30) <= a.data_hora or atual >= a.data_hora + timedelta(minutes=a.duracao))
                        for a in agendados
                    )
                    if not conflito and (data > hoje or atual.time() > datetime.now().time()):
                        disponiveis.append({
                            'inicio': atual.isoformat(),
                            'fim': (atual + timedelta(minutes=30)).isoformat()
                        })
                    atual += timedelta(minutes=30)

            return disponiveis
        except Exception as e:
            print(f"Erro ao listar horários: {e}")
            return []