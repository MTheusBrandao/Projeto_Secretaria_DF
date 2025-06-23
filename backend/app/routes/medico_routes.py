from flask import Blueprint, request, jsonify
from ..services.medico_service import MedicoService

bp = Blueprint('medicos', __name__, url_prefix='/api/medicos')


@bp.route('/', methods=['GET'])
def listar_todos():
    medicos = MedicoService.listar_todos()
    return jsonify(medicos), 200

@bp.route('/', methods=['POST'])
def cadastrar():
    dados = request.get_json()
    medico, erro, status = MedicoService.cadastrar_medico(dados)

    if erro:
        return jsonify(erro), status

    return jsonify(medico.to_dict()), status

@bp.route('/<int:medico_id>', methods=['GET'])
def obter(medico_id):
    medico = MedicoService.obter_medico(medico_id)
    if not medico:
        return jsonify({'erro': 'Médico não encontrado'}), 404
    return jsonify(medico.to_dict()), 200

@bp.route('/<int:medico_id>', methods=['PUT'])
def atualizar(medico_id):
    dados = request.get_json()
    medico, erro = MedicoService.atualizar_medico(medico_id, dados)

    if erro:
        return jsonify(erro['erro']), erro.get('status_code', 400)
    
    return jsonify(medico.to_dict()), 200