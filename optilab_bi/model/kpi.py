
from sqlalchemy import event

from .base import ModelBase
from optilab_bi import db
from optilab_bi.helpers import input_audit_data_on_insert, input_audit_data_on_update


class Kpi(ModelBase, db.Model):
    average_billing = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=False)
    average_order_quantity = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=False)
    average_tm = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=False)
    average_quantity_pieces = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=False)
    last_day_billing = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=True)
    last_day_order_quantity = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=True)
    last_day_tm = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=True)
    last_day_quantity_pieces = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=True)
    budget_billing = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=True)
    budget_order_quantity = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=True)
    budget_tm = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=True)
    budget_quantity_pieces = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=True)
    month = db.Column(db.Integer(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    business_code = db.Column(db.Integer(), nullable=False)
    

event.listen(Kpi, 'before_insert', input_audit_data_on_insert)
event.listen(Kpi, 'before_update', input_audit_data_on_update)
