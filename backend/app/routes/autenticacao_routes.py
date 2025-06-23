from flask import Blueprint, request, jsonify
from ..services.autenticacao_service import AutenticacaoService

bp = Blueprint('autenticacao', __name__, url_prefix='/api/auth')

@bp.route('/registro', methods=['POST'])
def registrar():
    dados = request.get_json()

    resultado, erro = AutenticacaoService.registrar_usuario(dados)
    
    if erro:
        return jsonify(erro), erro[1] if isinstance(erro, tuple) else 400

    return jsonify(resultado), 201


@bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()

    resultado, erro = AutenticacaoService.login(dados)
    
    if erro:
        return jsonify(erro), erro[1] if isinstance(erro, tuple) else 401

    return jsonify(resultado), 200
