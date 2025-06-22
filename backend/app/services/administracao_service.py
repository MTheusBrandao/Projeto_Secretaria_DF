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
                'nome': esp.nome,
                'codigo': esp.codigo,
                'descricao': esp.descricao
            }
            for esp in especialidades
        ]

    @staticmethod
    def cadastrar_especialidade(dados):
        try:
            print("Iniciando cadastro de especialidade")  # Log de depuração
        
            nova = Especialidade(
                nome=dados['nome'],
                codigo=dados.get('codigo'),
                descricao=dados.get('descricao'),
                ativo=True
            )
            
            db.session.add(nova)
            db.session.commit()
            
            print("Especialidade cadastrada com sucesso")  # Log de depuração
            return nova, None
            
        except Exception as e:
            print(f"Erro no cadastro: {str(e)}")  # Log de depuração
            return None, {'erro': str(e)}

    @staticmethod
    def atualizar_especialidade(especialidade_id, dados):
        esp = Especialidade.query.get(especialidade_id)
        if not esp or not esp.is_active:
            return None, {'erro': 'Especialidade não encontrada', 'status_code': 404}
        try:
            esp.nome = dados.get('nome', esp.nome)
            esp.codigo = dados.get('codigo', esp.codigo)
            esp.descricao = dados.get('descricao', esp.descricao)
            db.session.commit()
            return esp, None
        except Exception as e:
            return None, {'erro': str(e)}
