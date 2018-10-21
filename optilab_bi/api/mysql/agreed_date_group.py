import logging

from optilab_bi.model import AgreedDateGroup
from optilab_bi.config import API_VERSION

logger = logging.getLogger(__name__)

def create_api(api):
    api.create_api(AgreedDateGroup,
                   methods=['GET', 'PATCH'],
                   url_prefix='/%s' % API_VERSION,
                   results_per_page=0,
                   primary_key='id',
                   preprocessors={
                   },
                   postprocessors={
                   })