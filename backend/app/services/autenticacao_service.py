from ..models.usuario import Usuario
from ..extensions import db
from flask_jwt_extended import create_access_token

class AutenticacaoService: 
    @staticmethod
    def registrar_usuario(dados):
        # Validação basica inicial
        campos_obrigatorios = ['email', 'senha', 'nome', 'cpf', 'telefone']
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                return None, {'erro': f'{campo} é obrigatorio'}, 400
        
        # Verificação de usuario existente
        if Usuario.query.filter_by(email=dados['email']).first():
            return None, {'erro': 'Email já cadastrado'}, 400
        
        # criar usuario
        usuario = Usuario(
            email=dados['email'],
            nome=dados['nome'],
            cpf=dados['cpf'],
            telefone=dados['telefone'],
            endereco=dados.get('endereco', '')
        )
        usuario.set_senha(dados['senha'])

        db.session.add(usuario)
        db.session.commit()

        return usuario, None, None
    
    @staticmethod
    def login(email, senha):
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_senha(senha):
            token = create_access_token(
                identity=usuario.id,
                additional_claims={'tipo': usuario.tipo, 'nome': usuario.nome}
            )
            return {'token': token, 'usuario': usuario}, None
        return None, {'erro': 'Credenciais invalidas'}