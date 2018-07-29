import logging
from urllib.parse import urlparse
from flask import Flask
from flask_cors import CORS
from flask_restless.manager import APIManager
from optilab_bi import config, db
from optilab_bi.api.firebird import rate_service, billing, report_products, buys_customers
from optilab_bi.api.mysql import budget, configuration, user, product, customer
import fdb



def create_blueprints(flask_app):
    flask_app.register_blueprint(rate_service.actions)
    flask_app.register_blueprint(billing.actions)
    flask_app.register_blueprint(report_products.actions)
    flask_app.register_blueprint(buys_customers.actions)

def create_apis(api):
    budget.create_api(api)
    configuration.create_api(api)
    user.create_api(api)
    product.create_api(api)
    customer.create_api(api)

LOGGER = logging.getLogger(__name__)

app = Flask(__name__, static_folder="../static", template_folder="../templates")

app.config.from_object(config)

LOGGER.info('Configurado Flask')

CORS(app)

LOGGER.info("Configurado Ext Flask CORS")

db.init_app(app)

LOGGER.info('Configurado Extensão Flask SQLAlchemy')

api = APIManager(app=app, flask_sqlalchemy_db=db)

create_apis(api)

create_blueprints(app)





