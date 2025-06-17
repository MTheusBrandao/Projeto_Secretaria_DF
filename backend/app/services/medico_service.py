from ..models.medico import Medico
from ..extensions import db

class MedicoService:
    @staticmethod
    def listar_medicos(especialidade_id=None, ativo=True):
        query = Medico.query.filter_by(aitvo=ativo)

        if especialidade_id:
            query = query.filter_by(especialidade_id=especialidade_id)

        return query.all(), None, 200
    
    @staticmethod
    def cadastrar_medico(dados):
        medico=Medico(
            nome=dados['nome'],
            crm=dados['crm'],
            especialidade_id=dados.get['especialidade_id']
        )

        db.session.add(medico)
        db.session.commit()

    @staticmethod
    def atualizar_medico(medico_id, dados):
        medico = Medico.query.get(medico_id)
        if not medico:
            return None, {'erro': 'Medico Não encontrado'}, 404
        
        if 'nome' in dados:
            medico.nome = dados['nome']
        if 'crm' in dados:
            medico.crm = dados['crm']
        if 'especialidade_id' in dados:
            medico.especialidade_id = dados['especialidade_id']
        if 'ativo' in dados:
            medico.ativo = dados['ativo']

        db.session.commit()
        return medico, None
    
    @staticmethod
    def obter_medico(medico_id):
        return Medico.query.get(medico_id)
    