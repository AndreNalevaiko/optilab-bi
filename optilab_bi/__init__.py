from optilab_bi import config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_user import FlaskUser
import fdb

db = SQLAlchemy()
db_metrics = create_engine(config.DATABASE_METRICS)
user_manager = FlaskUser()

def get_connection():
    return fdb.connect(dsn='/home/andre/Documentos/databases/sgo.fdb', user='sysdba', password='masterkey', charset='latin1')
