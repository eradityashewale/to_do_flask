# Authentication decorator
from functools import wraps
from flask import request

API_KEY = 'sfsfsdggekgjk35j436j457ggeljt3kjl5kj37jknhn'

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if api_key and api_key == API_KEY:
            return f(*args, **kwargs)
        else:
            return {"error": "Unauthorized access"}, 401
    return decorated_function