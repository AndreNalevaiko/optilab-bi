import logging

from optilab_bi.model import Budget
from optilab_bi.config import API_VERSION

from .util import check_authentication

logger = logging.getLogger(__name__)


def create_api(api):
    api.create_api(Budget,
                   methods=['GET', 'POST', 'PATCH'],
                   url_prefix='/%s' % API_VERSION,
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