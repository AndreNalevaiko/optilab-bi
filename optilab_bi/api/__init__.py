import logging
from urllib.parse import urlparse
from flask import Flask
from flask_cors import CORS
from flask_restless.manager import APIManager
from optilab_bi import config, db, user_manager
from optilab_bi.api.firebird import rate_service, billing, report_products, buys_customers, kpi
from optilab_bi.api.mysql import budget, configuration, user, product, customer, kpi as kpi_api, agreed_date_group
import fdb



def create_blueprints(flask_app):
    flask_app.register_blueprint(rate_service.actions)
    flask_app.register_blueprint(billing.actions)
    flask_app.register_blueprint(report_products.actions)
    flask_app.register_blueprint(buys_customers.actions)
    flask_app.register_blueprint(kpi.actions)
    flask_app.register_blueprint(user.actions)

def create_apis(api):
    budget.create_api(api)
    configuration.create_api(api)
    user.create_api(api)
    product.create_api(api)
    customer.create_api(api)
    kpi_api.create_api(api)
    agreed_date_group.create_api(api)

def flask_user(app):
    from optilab_bi.model import User

    user_manager.init_app(app, user_entity=User, sqlalchemy_db=db)


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

LOGGER.info('Configurado Apis')

create_blueprints(app)

LOGGER.info('Configurado Blueprints')

flask_user(app)

LOGGER.info('Configurado Flask User')




