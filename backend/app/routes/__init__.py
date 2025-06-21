from .agendamento_routes import bp as agendamento_bp
from .autenticacao_routes import bp as autenticacao_bp
from .horario_routes import bp as horario_bp
from .medico_routes import bp as medico_bp
from .administracao_routes import bp as adm_bp

__all__ = [
    'agendamento_bp',
    'autenticacao_bp',
    'horario_bp',
    'medico_bp',
    'adm_bp'
]