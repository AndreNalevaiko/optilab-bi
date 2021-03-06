import logging

from optilab_bi.model import Configuration
from optilab_bi.config import API_VERSION

# actions = create_actions_blueprint(BankReceive, api_version=API_VERSION)

logger = logging.getLogger(__name__)


def get_config(key):
    config = Configuration.query.filter_by(key=key).one_or_none()
    
    if config:
        return config.value
        
    return config


def create_api(api):
    api.create_api(Configuration,
                   methods=['GET', 'POST'],
                   url_prefix='/%s' % API_VERSION,
                   results_per_page=10,
                   primary_key='id',
                   preprocessors={
                   },
                   postprocessors={
                   })