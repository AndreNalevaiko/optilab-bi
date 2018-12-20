import logging, datetime

from optilab_bi.model import CustomerBillingReport, NumberActiveCustomers
from optilab_bi.api.firebird.buys_customers import generate_current_day_amount
from optilab_bi.config import API_VERSION

from .util import check_authentication

logger = logging.getLogger(__name__)

def before_get_number_active(search_params=None, **kw):
    param_date = datetime.datetime.strptime(search_params['filters'][0]['val'], '%Y-%m-%d')

    date = {
        'day': str(param_date.day),
        'month': str(param_date.month),
        'year': str(param_date.year),
    }
    
    generate_current_day_amount(date)

def create_api(api):
    api.create_api(CustomerBillingReport,
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

    api.create_api(NumberActiveCustomers,
                   methods=['GET'],
                   url_prefix='/%s' % API_VERSION,
                   results_per_page=0,
                   primary_key='id',
                   preprocessors={
                       'GET_SINGLE': [
                           check_authentication(['user'])
                       ],
                       'GET_MANY': [
                           check_authentication(['user']),
                           before_get_number_active
                       ]
                   },
                   postprocessors={
                   })