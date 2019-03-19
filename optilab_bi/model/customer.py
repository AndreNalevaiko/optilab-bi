from sqlalchemy import event

from .base import ModelBase
from optilab_bi import db
from optilab_bi.helpers import input_audit_data_on_insert, input_audit_data_on_update

class CustomerBillingReport(ModelBase, db.Model):
    customer_code = db.Column(db.Integer(), nullable=False)
    customer_name = db.Column(db.String(128), nullable=False)
    seller = db.Column(db.Integer(), nullable=False)
    current_value = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=False)
    latest_value = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=False)
    variation = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=False)
    month = db.Column(db.Integer(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.Date())

class NumberActiveCustomers(ModelBase, db.Model):
    average_latest_year = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=False)
    number_current_day = db.Column(db.Integer(), nullable=False)
    number_current_month = db.Column(db.Integer(), nullable=False)
    number_latest_day = db.Column(db.Integer(), nullable=False)
    number_latest_month = db.Column(db.Integer(), nullable=False)
    seller = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.Date() , nullable=False)

event.listen(CustomerBillingReport, 'before_insert', input_audit_data_on_insert)
event.listen(CustomerBillingReport, 'before_update', input_audit_data_on_update)

event.listen(NumberActiveCustomers, 'before_insert', input_audit_data_on_insert)
event.listen(NumberActiveCustomers, 'before_update', input_audit_data_on_update)