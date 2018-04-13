from flask_sqlalchemy import SQLAlchemy
import fdb
# from flask_configuration.core import FlaskConfiguration

db = SQLAlchemy()

# engine = fdb.connect(dsn='D:\sgo\sgo.fdb', user='sysdba', password='ffracert', charset='latin1')
engine = fdb.connect(dsn='D:\sgo\sgo.fdb', user='sysdba', password='masterkey', charset='latin1')
# engine = fdb.connect(dsn='192.168.10.12:sgo', user='sysdba', password='ffracert', charset='latin1')

db2 = engine.cursor()

# flask_configuration = FlaskConfiguration()