import logging
from urllib.parse import urlparse
from optilab_bi import config, db
from optilab_bi.api import rate_service, billing, abstract_products
import fdb
from flask import Flask
from flask_cors import CORS


def create_blueprints(flask_app):
    flask_app.register_blueprint(rate_service.actions)
    flask_app.register_blueprint(billing.actions)
    flask_app.register_blueprint(abstract_products.actions)

LOGGER = logging.getLogger(__name__)

app = Flask(__name__, static_folder="../static", template_folder="../templates")

app.config.from_object(config)

LOGGER.info('Configurado Flask')

CORS(app)

LOGGER.info("Configurado Ext Flask CORS")

db.init_app(app)

LOGGER.info('Configurado Extensão Flask SQLAlchemy')

create_blueprints(app)





