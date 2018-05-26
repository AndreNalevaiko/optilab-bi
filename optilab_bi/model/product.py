
from enum import Enum
from sqlalchemy import event

from .base import ModelBase
from optilab_bi import db
from optilab_bi.helpers import input_audit_data_on_insert, input_audit_data_on_update


class ReportStatus(Enum):
    OPENED = 'OPENED'
    CLOSED = 'CLOSED'
    

class Product(ModelBase, db.Model):
    label = db.Column(db.String(64), nullable=False)
    like_or = db.Column(db.String(256), nullable=True)
    like_and = db.Column(db.String(256), nullable=True)
    color = db.Column(db.Integer(), nullable=True)
    process = db.Column(db.String(32), nullable=True)
    show_in_abstract = db.Column(db.Boolean, nullable=False)


class ReportProducts(ModelBase, db.Model):
    brand = db.Column(db.String(128), nullable=False)
    label = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Enum(*[e.value for e in ReportStatus]), nullable=False)
    business_code = db.Column(db.Integer(), nullable=False)
    month = db.Column(db.Integer(), nullable=False)
    latest_year = db.Column(db.Integer(), nullable=False)
    current_year = db.Column(db.Integer(), nullable=False)
    qtd_latest_year = db.Column(db.Integer(), nullable=False)
    value_latest_year = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=False)
    qtd_current_year = db.Column(db.Integer(), nullable=False)
    value_current_year = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=False)
    

event.listen(Product, 'before_insert', input_audit_data_on_insert)
event.listen(Product, 'before_update', input_audit_data_on_update)

event.listen(ReportProducts, 'before_insert', input_audit_data_on_insert)
event.listen(ReportProducts, 'before_update', input_audit_data_on_update)