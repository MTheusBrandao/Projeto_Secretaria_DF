# routes/administracao_routes.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..services.administracao_service import AdministracaoService
from ..utils.decoradores import tratamento_erros

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.route('/regional-admins', methods=['GET'])
@jwt_required()
@tratamento_erros
def listar_regioes_administrativas():
    ras = AdministracaoService.listar_regioes_administrativas()
    return jsonify(ras), 200

@bp.route('/specialties', methods=['GET'])
@jwt_required()
@tratamento_erros
def listar_especialidades():
    especialidades = AdministracaoService.listar_especialidades()
    return jsonify(especialidades), 200

@bp.route('/specialties', methods=['POST'])
@jwt_required()
@tratamento_erros
def cadastrar_especialidade():
    dados = request.get_json()
    especialidade, erro = AdministracaoService.cadastrar_especialidade(dados)
    if erro:
        return jsonify(erro), 400
    return jsonify({
        'id': especialidade.id,
        'nome': especialidade.name,
        'codigo': especialidade.code,
        'descricao': especialidade.description
    }), 201

@bp.route('/specialties/<int:especialidade_id>', methods=['PUT'])
@jwt_required()
@tratamento_erros
def atualizar_especialidade(especialidade_id):
    dados = request.get_json()
    especialidade, erro = AdministracaoService.atualizar_especialidade(especialidade_id, dados)
    if erro:
        return jsonify(erro), erro.get('status_code', 400)
    return jsonify({
        'id': especialidade.id,
        'nome': especialidade.name,
        'codigo': especialidade.code,
        'descricao': especialidade.description
    }), 200
