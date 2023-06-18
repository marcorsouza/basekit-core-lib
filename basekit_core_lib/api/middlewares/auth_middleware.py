import os
import functools
import jwt
import requests

from enum import Enum
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from api.models.user_permissions_view import UserPermissions
from utils.file_utils import get_env
from config.helpers import config

def authenticate(func):
    @wraps(func)
    @jwt_required(optional=True)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:                              
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401

        return jsonify({'error': 'Missing authorization header'}), 401

    return wrapper

def authorize(tag_name: str, authorize):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Missing or invalid authorization header'}), 401

            if isinstance(authorize, Enum):
                authorize_value = authorize.value
            elif isinstance(authorize, str):
                authorize_value = authorize
            else:
                authorize_value = None

            username = get_jwt_identity()
            auth_token = auth_header.replace('Bearer ', '')
            if config.API_AUTH_URL is not None:
                url = f'{config.API_AUTH_URL}/check'
                print(url)
                has_permission = check_permission_with_auth(username, tag_name, config.APPLICATION_ACRONYM, authorize_value, url, auth_token)
            else:
                print('local')
                has_permission = __check_permission(username, tag_name, config.APPLICATION_ACRONYM, authorize_value)

            if has_permission:
                return func(*args, **kwargs)
            else:
                return jsonify({'error': 'Usuário não tem permissão para a ação.'}), 401

        return wrapper

    return decorator

def check_permission_with_auth(username, tag_name, acronym, action_name, auth_url, auth_token):
    # Realiza a autenticação com a API
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.post(auth_url, headers=headers, json={
        'username': username,
        'tag_name': tag_name,
        'acronym': acronym,
        'action_name': action_name
    })

    # Verifica o resultado da autenticação
    if response.status_code == 200:
        return True
    else:
        return False

def __check_permission(username, tag_name, acronym, action_name):
    
    user_permissions = UserPermissions.get_user_permissions(
        username=username,
        tag_name=tag_name,
        acronym=acronym,
        action_name=action_name
    )
    
    if user_permissions is not None :
        # Usuário tem permissão
        return True
     
    return False

class Authorize(Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"