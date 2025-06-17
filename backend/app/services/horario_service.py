from datetime import time, timedelta, datetime
from ..models import HorarioMedico, Medico, Agendamento
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

        horario = HorarioMedico(
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
        query = HorarioMedico.query.filter_by(medico_id=medico_id)

        if apenas_ativos:
            query = query.filter_by(ativo=True)

        return query.order_by(HorarioMedico.dia_semana, HorarioMedico.hora_inicio).all()
    
    @staticmethod
    def verificar_disponibilidade(medico_id, data, duracao_minutos=30):
        """
        Verifica se um médico está disponível em um determinado horário
        
        Args:
            medico_id: ID do médico
            data_hora: DateTime do agendamento pretendido
            duracao_minutos: Duração em minutos (padrão 30)
            
        Returns:
            tuple: (disponivel, mensagem) ou (None, erro)
        """
        try:
            if isinstance(data_hora, str):
                data_hora = datetime.fromisoformat(data_hora)
                
            # 1. Verificar se há horário cadastrado para esse dia
            dia_semana = data_hora.weekday()
            hora_consulta = data_hora.time()
            fim_consulta = (data_hora + timedelta(minutes=duracao_minutos)).time()
            
            horario = HorarioMedico.query.filter(
                HorarioMedico.medico_id == medico_id,
                HorarioMedico.dia_semana == dia_semana,
                HorarioMedico.hora_inicio <= hora_consulta,
                HorarioMedico.hora_fim >= fim_consulta,
                HorarioMedico.ativo == True
            ).first()
            
            if not horario:
                return False, "Médico não atende neste horário"
                
            # 2. Verificar conflito com agendamentos existentes
            conflito = Agendamento.query.filter(
                Agendamento.medico_id == medico_id,
                Agendamento.data_hora < data_hora + timedelta(minutes=duracao_minutos),
                Agendamento.data_hora + timedelta(minutes=Agendamento.duracao) > data_hora,
                Agendamento.status == 'agendado'
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
        """
        Lista todos os horários disponíveis de um médico em uma data específica
        
        Args:
            medico_id: ID do médico
            data: Data no formato 'YYYY-MM-DD' ou objeto date
            
        Returns:
            list: Lista de horários disponíveis
        """
        try:
            if isinstance(data, str):
                data = datetime.strptime(data, '%Y-%m-%d').date()
                
            dia_semana = data.weekday()
            data_atual = datetime.now().date()
            
            # Obter horário de trabalho do médico
            horarios_trabalho = HorarioMedico.query.filter(
                HorarioMedico.medico_id == medico_id,
                HorarioMedico.dia_semana == dia_semana,
                HorarioMedico.ativo == True
            ).order_by(HorarioMedico.hora_inicio).all()
            
            if not horarios_trabalho:
                return []
                
            # Obter agendamentos do dia
            inicio_dia = datetime.combine(data, time.min)
            fim_dia = datetime.combine(data, time.max)
            
            agendamentos = Agendamento.query.filter(
                Agendamento.medico_id == medico_id,
                Agendamento.data_hora.between(inicio_dia, fim_dia),
                Agendamento.status == 'agendado'
            ).order_by(Agendamento.data_hora).all()
            
            disponiveis = []
            
            for horario in horarios_trabalho:
                slot_inicio = datetime.combine(data, horario.hora_inicio)
                slot_fim = datetime.combine(data, horario.hora_fim)
                
                # Se for no passado, pular
                if data == data_atual and slot_inicio.time() < datetime.now().time():
                    continue
                    
                # Gerar slots de 30 minutos
                current_slot = slot_inicio
                while current_slot + timedelta(minutes=30) <= slot_fim:
                    fim_slot = current_slot + timedelta(minutes=30)
                    
                    # Verificar conflito com agendamentos
                    conflito = False
                    for agendamento in agendamentos:
                        agendamento_fim = agendamento.data_hora + timedelta(minutes=agendamento.duracao)
                        if not (fim_slot <= agendamento.data_hora or current_slot >= agendamento_fim):
                            conflito = True
                            break
                            
                    if not conflito:
                        disponiveis.append({
                            'inicio': current_slot.isoformat(),
                            'fim': fim_slot.isoformat()
                        })
                        
                    current_slot += timedelta(minutes=30)
                    
            return disponiveis
            
        except Exception as e:
            print(f"Erro ao listar horários: {str(e)}")
            return []