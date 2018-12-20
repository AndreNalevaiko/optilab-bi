import logging
from optilab_bi import user_manager

from .util import check_authentication

from optilab_bi.model import ReportProducts
from optilab_bi.config import API_VERSION

logger = logging.getLogger(__name__)

def create_api(api):
    api.create_api(ReportProducts,
                   methods=['GET'],
                   url_prefix='/%s' % API_VERSION,
                   results_per_page=0,
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