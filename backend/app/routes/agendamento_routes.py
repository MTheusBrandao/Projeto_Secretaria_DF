from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.agendamento_service import ServicoAgendamento
from datetime import datetime

bp = Blueprint('agendamentos', __name__, url_prefix='/api/agendamentos')

@bp.route('/', methods=['POST'])
@jwt_required()
def criar():
    dados = request.get_json()
    usuario_id = get_jwt_identity()

    try:
        data_hora = datetime.fromisoformat(dados['data_hora'])
    except ValueError:
        return jsonify({'erro': 'Formato de data/hora invalido'}), 400
    
    agendamento, erro = ServicoAgendamento.criar_agendamento(
        paciente_id=usuario_id,
        medico_id=dados['medico_id'],
        data_hora=data_hora,
        observacoes=dados.get('observacoes')
    )

    if erro:
        return jsonify(erro), erro.get('status_code', 400)
    
    return jsonify(agendamento.to_dict()), 201
    
@bp.route('/', methods=['GET'])
@jwt_required()
def listar():
    usuario_id = get_jwt_identity()
    medico_id = request.args.get('medico_id')

    agendamentos = ServicoAgendamento.listar_agendamentos(
        medico_id=medico_id,
        paciente_id=usuario_id
    )

    return jsonify([a.to_dict() for a in agendamentos]), 200

@bp.route('/<int:agendamento_id>', methods=['DELETE'])
@jwt_required()
def cancelar(agendamento_id):
    usuario_id = get_jwt_identity()
    agendamento, erro = ServicoAgendamento.cancelar_agendamento(agendamento_id, usuario_id)

    if erro:
        return jsonify(erro), erro.get('status_code', 400)
    
    return jsonify(agendamento.to_dict()), 200