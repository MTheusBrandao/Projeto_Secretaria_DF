from flask import Blueprint, request, jsonify
from ..services.autenticacao_service import AutenticacaoService

bp = Blueprint('autenticacao', __name__, url_prefix='/api/auth')

@bp.route('/registrar', methods=['POST'])
def registrar():
    dados = request.get_json()
    usuario, erro, status = AutenticacaoService.registrar_usuario(dados)

    if not usuario:
        return jsonify(erro or {'erro': 'Erro interno'}), status or 400

    return jsonify({
        'mensagem': 'Usuário registrado com sucesso',
        'usuario': {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email
        }
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    resultado, erro = AutenticacaoService.login(dados.get('email'), dados.get('senha'))
    
    if erro:
        return jsonify(erro), 401
    
    return jsonify(resultado), 200