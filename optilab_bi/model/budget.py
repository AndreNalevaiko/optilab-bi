
from sqlalchemy import event

from .base import ModelBase
from optilab_bi import db
from optilab_bi.helpers import input_audit_data_on_insert, input_audit_data_on_update


class Budget(ModelBase, db.Model):
    month = db.Column(db.Integer(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    value = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=False)
    business_code = db.Column(db.Integer(), nullable=False)
    

event.listen(Budget, 'before_insert', input_audit_data_on_insert)
event.listen(Budget, 'before_update', input_audit_data_on_update)