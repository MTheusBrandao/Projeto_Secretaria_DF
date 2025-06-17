from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..services.horario_service import HorarioService

bp = Blueprint('horarios', __name__, url_prefix='/api/horarios')

@bp.route('/', methods=['POST'])
@jwt_required()
def cadastrar_horario():
    dados = request.get_json()
    horario, erro = HorarioService.cadastrar_horario(
        medico_id=dados['medico_id'],
        dia_semana=dados['dia_semana'],
        hora_inicio=dados['hora_inicio'],
        hora_fim=dados['hora_fim']
    )
    
    if erro:
        return jsonify(erro), erro.get('status_code', 400)
        
    return jsonify(horario.to_dict()), 201

@bp.route('/medico/<int:medico_id>', methods=['GET'])
def listar_horarios_medico(medico_id):
    apenas_ativos = request.args.get('apenas_ativos', 'true').lower() == 'true'
    horarios = HorarioService.listar_horarios(medico_id, apenas_ativos)
    return jsonify([h.to_dict() for h in horarios]), 200