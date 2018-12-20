from flask_sqlalchemy import SQLAlchemy
from flask_user import FlaskUser
import fdb

db = SQLAlchemy()
user_manager = FlaskUser()

def get_connection():
    return fdb.connect(dsn='/home/andre/Documentos/databases/sgo.fdb', user='sysdba', password='masterkey', charset='latin1')
