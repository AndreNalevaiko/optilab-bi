import logging
from flask import Blueprint, jsonify
from optilab_bi import user_manager

from optilab_bi.model import User
from optilab_bi.config import API_VERSION

from .util import prepare_response, check_authentication

actions = Blueprint('user', __name__, url_prefix='/user')

logger = logging.getLogger(__name__)

exclude_user_columns = [
    'active',
    'confirmed_at',
    'current_login_at',
    'current_login_ip',
    'last_login_at',
    'last_login_ip',
    'login_count',
    'password',
    'profile_photo_id'
]

@actions.route('/me', methods=['GET'])
@user_manager.auth_required('user')
def me(auth_data=None):
    user = auth_data['user']
    response = prepare_response(user, exclude_user_columns)
    return jsonify(response), 200


def create_api(api):
    api.create_api(User,
                   methods=['GET'],
                   url_prefix='/%s' % API_VERSION,
                   exclude_columns=exclude_user_columns,
                   results_per_page=10,
                   primary_key='id',
                   preprocessors={
                       'GET_SINGLE': [
                           check_authentication(['user'])
                       ],
                       'GET_MANY': [
                           check_authentication(['user'])
                       ]
                   },
                   postprocessors={
                   })