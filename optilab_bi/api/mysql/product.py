import logging

from optilab_bi.model import Product, ReportProducts
from optilab_bi.config import API_VERSION

logger = logging.getLogger(__name__)

def create_api(api):
    api.create_api(Product,
                   methods=['GET', 'POST', 'PATCH'],
                   url_prefix='/%s' % API_VERSION,
                   results_per_page=20,
                   primary_key='id',
                   preprocessors={
                   },
                   postprocessors={
                   })

    api.create_api(ReportProducts,
                   methods=['GET'],
                   url_prefix='/%s' % API_VERSION,
                   results_per_page=20,
                   primary_key='id',
                   preprocessors={
                   },
                   postprocessors={
                   })