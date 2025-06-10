from flask import Blueprint, request, jsonify
from ..services.medico_service import MedicoService

bp = Blueprint('medicos', __name__, url_prefix='/api/medicos')

@bp.route('/', methods=['GET'])
def listar():
    especialidade_id = request.args.get('especialidade_id')
    medicos = MedicoService.listar_medicos(especialidade_id=especialidade_id)
    return jsonify([medico.to_dict() for medico in medicos]), 200

@bp.route('/', methods=['POST'])
def cadastrar():
    dados = request.get_json()
    medico, erro = MedicoService.cadastrar_medico(dados)

    if erro:
        return jsonify(erro), 400
    
    return jsonify(medico.to_dict()), 201

@bp.route('/<int:medico_id>', methods=['PUT'])
def obter(medico_id):
    medico = MedicoService.obter_medico(medico_id)
    if not medico:
        return jsonify({'erro': 'Médico não encontrado'}), 404

@bp.route('/<int:medico_id>', methods=['PUT'])
def atualizar(medico_id):
    dados = request.get_json()
    medico, erro = MedicoService.atualizar_medico(medico_id, dados)

    if erro:
        return jsonify(erro['erro']), erro.get('status_code', 400)
    
    return jsonify(medico.to_dict()), 200