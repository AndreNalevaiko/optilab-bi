import logging

from optilab_bi.model import Product
from optilab_bi.config import API_VERSION

# actions = create_actions_blueprint(BankReceive, api_version=API_VERSION)

logger = logging.getLogger(__name__)


def get_products_abstract():
    products = Product.query.filter_by(show_in_abstract=True).all()
    return products


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