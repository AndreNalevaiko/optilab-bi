from optilab_bi import config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_user import FlaskUser
import fdb

db = SQLAlchemy()
db_metrics = create_engine(config.DATABASE_METRICS, pool_recycle=1800)
user_manager = FlaskUser()

def get_connection():
    return fdb.connect(
        dsn=config.DATABASE_SGO_URL,
        user=config.DATABASE_SGO_USER,
        password=config.DATABASE_SGO_PASS,
        charset='latin1')
