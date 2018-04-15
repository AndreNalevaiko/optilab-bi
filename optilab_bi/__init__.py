from flask_sqlalchemy import SQLAlchemy
import fdb
# from flask_configuration.core import FlaskConfiguration

db = SQLAlchemy()

engine = fdb.connect(dsn='/home/andre/Documentos/databases/sgo.fdb', user='sysdba', password='masterkey', charset='latin1')

db2 = engine.cursor()

# flask_configuration = FlaskConfiguration()