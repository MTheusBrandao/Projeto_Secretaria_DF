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

    agenda_id = dados.get('agenda_id')
    data = dados.get('data')
    horario = dados.get('horario')

    if not all([agenda_id, data, horario]):
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400

    agendamento, erro, status = ServicoAgendamento.criar_agendamento(
    usuario_id, agenda_id, data, horario
)
    if erro:
        return jsonify(erro), status
    return jsonify(agendamento), status
    
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
    agendamento, erro, status = ServicoAgendamento.cancelar_agendamento(agendamento_id, usuario_id)
    
    if erro:
        return jsonify(erro), status
    
    return jsonify({'mensagem': 'Agendamento cancelado com sucesso'}), status
