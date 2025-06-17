from functools import wraps
from flask import jsonify

def tratamento_erros(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    return wrapped