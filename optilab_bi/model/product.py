
from sqlalchemy import event

from .base import ModelBase
from optilab_bi import db
from optilab_bi.helpers import input_audit_data_on_insert, input_audit_data_on_update


class Product(ModelBase, db.Model):
    label = db.Column(db.String(64), nullable=False)
    like_or = db.Column(db.String(256), nullable=True)
    like_and = db.Column(db.String(256), nullable=True)
    color = db.Column(db.Integer(), nullable=True)
    process = db.Column(db.String(32), nullable=True)
    show_in_abstract = db.Column(db.Boolean, nullable=False)
    

event.listen(Product, 'before_insert', input_audit_data_on_insert)
event.listen(Product, 'before_update', input_audit_data_on_update)