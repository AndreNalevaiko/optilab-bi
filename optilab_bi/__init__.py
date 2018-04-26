from flask_sqlalchemy import SQLAlchemy
import fdb

db = SQLAlchemy()

connection = fdb.connect(dsn='/home/andre/Documentos/databases/sgo.fdb', user='sysdba', password='masterkey', charset='latin1')
