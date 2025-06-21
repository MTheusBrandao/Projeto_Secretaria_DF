from ..models import RegiaoAdministrativa, Especialidade
from ..extensions import db

class AdministracaoService:
    @staticmethod
    def listar_regioes_administrativas():
        ras = RegiaoAdministrativa.query.filter_by(is_active=True).all()
        return [
            {
                'id': ra.id,
                'nome': ra.nome,
                'codigo': ra.codigo,
                'endereco': ra.endereco,
                'telefone': ra.telefone
            }
            for ra in ras
        ]

    @staticmethod
    def listar_especialidades():
        especialidades = Especialidade.query.filter_by(is_active=True).all()
        return [
            {
                'id': esp.id,
                'nome': esp.name,
                'codigo': esp.code,
                'descricao': esp.description
            }
            for esp in especialidades
        ]

    @staticmethod
    def cadastrar_especialidade(dados):
        try:
            nova = Especialidade(
                name=dados['nome'],
                code=dados.get('codigo'),
                description=dados.get('descricao'),
                is_active=True
            )
            db.session.add(nova)
            db.session.commit()
            return nova, None
        except Exception as e:
            return None, {'erro': str(e)}

    @staticmethod
    def atualizar_especialidade(especialidade_id, dados):
        esp = Especialidade.query.get(especialidade_id)
        if not esp or not esp.is_active:
            return None, {'erro': 'Especialidade não encontrada', 'status_code': 404}
        try:
            esp.name = dados.get('nome', esp.name)
            esp.code = dados.get('codigo', esp.code)
            esp.description = dados.get('descricao', esp.description)
            db.session.commit()
            return esp, None
        except Exception as e:
            return None, {'erro': str(e)}
