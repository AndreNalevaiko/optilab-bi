from flask_sqlalchemy import SQLAlchemy
import fdb

db = SQLAlchemy()

engine = fdb.connect(dsn='/home/andre/Documentos/databases/sgo.fdb', user='sysdba', password='masterkey', charset='latin1')

db2 = engine.cursor()
