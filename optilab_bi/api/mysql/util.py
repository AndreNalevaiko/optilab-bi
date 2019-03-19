import collections
from flask_restless.helpers import to_dict, get_relations

# TODO aqui
from functools import wraps
from flask import Response, request, current_app, jsonify
from flask.blueprints import Blueprint
from flask_restless.views import ProcessingException
from flask_sqlalchemy import Model
from flask_login import current_user
from flask_security import auth_required, roles_required
from optilab_bi.model import User

from optilab_bi import user_manager

def prepare_response(instance, exclude_columns=None):
    """
    Prepara um objeto para ser retornado como um JSON na resposta de uma requisição.

    :param instance: o objeto que será retornado.
    :param model: a classe do objeto que será retornado.
    :param exclude_columns: os campos que não devem ser retornados no objeto.
    :return: um objeto pronto para ser convertido para JSON.
    """

    if not isinstance(instance, collections.Iterable):
        relations = frozenset(get_relations(type(instance)))
        relations_suitable = list()
        if exclude_columns:
            for r in relations:
                if r not in exclude_columns:
                    relations_suitable.append(r)

        result = to_dict(instance, exclude=exclude_columns)
        for relation in relations_suitable:
            relation_exclude_columns = None
            if exclude_columns:
                for c in exclude_columns:
                    if isinstance(c, dict) and relation in c:
                        relation_exclude_columns = c[relation]
                        break

            result[relation] = prepare_response(getattr(instance, relation), exclude_columns=relation_exclude_columns)

        return result

    result_list = list()
    for obj in instance:
        result_list.append(prepare_response(obj, exclude_columns=exclude_columns))

    return result_list

# TODO começa aqui

def not_authenticated():
    raise ProcessingException(description='Not authenticated!', code=401)


def unauthorized():
    raise ProcessingException(description='Unauthorized', code=401)


def forbidden():
    raise ProcessingException(description='Forbidden', code=403)


def bad_request(message='Bad Request'):
    raise ProcessingException(description=message, code=400)

@auth_required('token', 'session')
def get_current_user():
    return current_user


def get_auth_data():
    auth_data = {}

    user = get_current_user()

    # Se o usuário não está autenticado então será retornado um Response 401
    if isinstance(user, Response) or not user.is_authenticated:
        return None

    auth_data['type'] = 'user'
    auth_data['user'] = User.query.get(user.id)
    return auth_data


def user_has_role(user, roles):
    """
    Função auxilizar que verifica se o usuário possui ao menos uma das roles informadas.
    :param user:
    :param roles:
    :return:
    """

    if not roles or len(roles) == 0:
        return True

    for role in roles:
        has_role = role in (role.name for role in user.roles)

        if has_role:
            return True

    return False


def raise_for_authentication_failed(auth_types=list(), user_roles_allowed=list()):
    """Verifica se existe usuário autenticado. Se não existir então lança uma exceção."""

    auth_data = user_manager.auth_data()

    if auth_data is None:
        unauthorized()

    if auth_data['type'] not in auth_types:
        unauthorized()

    if auth_data['type'] == 'user':
        if not user_has_role(auth_data['user'], user_roles_allowed):
            unauthorized()


def check_authentication(auth_types=list(), user_roles_allowed=list()):
    return lambda **kw: raise_for_authentication_failed(auth_types, user_roles_allowed)


def auth_required(*args, **kwargs):
    """
    Decorator que verifica o token de autenticação informado na requisição.
    Excemplo de utilização:
    @actions.route('/me', methods=['POST'])
    @auth_required('user', user_roles_allowed=['master'])
    def me(auth_data=None):
        return {'name': 'josé'}
    :param args:
    :param kwargs:
    :return:
    """

    auth_types = [auth_type for auth_type in args]
    user_roles_allowed = []
    if 'user_roles_allowed' in kwargs:
        user_roles_allowed = kwargs['user_roles_allowed']

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            unauthorized = jsonify(error='Unauthorized'), 401

            auth_data = get_auth_data()
            if auth_data is None or auth_data['type'] not in auth_types:
                return unauthorized

            if auth_data['type'] == 'user':
                if not user_has_role(auth_data['user'], user_roles_allowed):
                    return unauthorized

            if 'auth_data' in fn.__code__.co_varnames:
                kwargs['auth_data'] = auth_data

            return fn(*args, **kwargs)

        return decorator

    return wrapper
