from ..models import RegiaoAdministrativa, Especialidade
from ..extensions import db

class AdministracaoService:
    @staticmethod
    def criar_regioes_administrativas_padrao():
        regioes = [
            {'nome': 'Plano Piloto', 'codigo': 'RA-I', 'endereco': 'Asa Norte - DF', 'telefone': '6133210001'},
            {'nome': 'Taguatinga', 'codigo': 'RA-III', 'endereco': 'Taguatinga Centro - DF', 'telefone': '6133210002'},
            {'nome': 'Ceilândia', 'codigo': 'RA-IX', 'endereco': 'Ceilândia Sul - DF', 'telefone': '6133210003'},
            {'nome': 'Samambaia', 'codigo': 'RA-XII', 'endereco': 'Samambaia Norte - DF', 'telefone': '6133210004'},
            {'nome': 'Gama', 'codigo': 'RA-II', 'endereco': 'Setor Central - DF', 'telefone': '6133210005'},
        ]

        inseridos = 0
        for regiao in regioes:
            existe = RegiaoAdministrativa.query.filter_by(codigo=regiao['codigo']).first()
            if not existe:
                nova = RegiaoAdministrativa(
                    nome=regiao['nome'],
                    codigo=regiao['codigo'],
                    endereco=regiao['endereco'],
                    telefone=regiao['telefone'],
                    ativo=True
                )
                db.session.add(nova)
                inseridos += 1

        if inseridos > 0:
            db.session.commit()
            return {'mensagem': f'{inseridos} regiões administrativas cadastradas.'}, 201
        else:
            return {'mensagem': 'Regiões já estavam cadastradas.'}, 200
        
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
