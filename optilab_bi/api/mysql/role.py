import logging
from flask import Blueprint, jsonify
from optilab_bi import user_manager

from optilab_bi.model import Role
from optilab_bi.config import API_VERSION

from .util import check_authentication

# actions = Blueprint('role', __name__, url_prefix='/role')

logger = logging.getLogger(__name__)

def create_api(api):
    api.create_api(Role,
                   methods=['GET'],
                   url_prefix='/%s' % API_VERSION,
                   results_per_page=10,
                   primary_key='id',
                   preprocessors={
                       'GET_SINGLE': [
                           check_authentication(['user'], user_roles_allowed=['admin'])
                       ],
                       'GET_MANY': [
                           check_authentication(['user'], user_roles_allowed=['admin'])
                       ]
                   },
                   postprocessors={
                   })