from flask_jwt_extended import create_access_token
from ..models.usuario import Usuario
from ..extensions import db
from datetime import timedelta

class AutenticacaoService: 

    @staticmethod
    def registrar_usuario(dados):
        campos_obrigatorios = ['email', 'senha', 'nome', 'cpf', 'telefone']
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                return None, {'erro': f'{campo} é obrigatório'}, 400

        if Usuario.query.filter_by(email=dados['email']).first():
            return None, {'erro': 'Email já cadastrado'}, 400
        
        if Usuario.query.filter_by(cpf=dados['cpf']).first():
            return None, {'erro': 'CPF já cadastrado'}, 400

        usuario = Usuario(
            email=dados['email'],
            nome=dados['nome'],
            cpf=dados['cpf'],
            telefone=dados['telefone'],
            tipo=dados.get('tipo', 'paciente')
        )
        usuario.set_senha(dados['senha'])

        db.session.add(usuario)
        db.session.commit()

        return {
            'mensagem': 'Usuário registrado com sucesso',
            'usuario': usuario.to_dict()
        }, None  # <-- Mantém padrão (resultado, erro)

    @staticmethod
    def login(dados):
        email = dados.get('email')
        senha = dados.get('senha')

        if not email or not senha:
            return None, {'erro': 'Email e senha obrigatórios'}, 400

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario or not usuario.check_senha(senha):
            return None, {'erro': 'Credenciais inválidas'}, 401

        access_token = create_access_token(
            identity=str(usuario.id),
            additional_claims={
                'tipo': usuario.tipo,
                'nome': usuario.nome
            },
            expires_delta=timedelta(hours=24)
        )

        return {'access_token': access_token}, None
