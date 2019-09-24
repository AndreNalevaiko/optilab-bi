
from sqlalchemy import event
from enum import Enum

from .base import ModelBase
from optilab_bi import db
from optilab_bi.helpers import input_audit_data_on_insert, input_audit_data_on_update

class TypeRef(Enum):
    BILLING = 'BILLING'
    PRODUCT_AMOUNT = 'PRODUCT_AMOUNT'
    PRODUCT_VALUE = 'PRODUCT_VALUE'
    CUSTOMERS_ACTIVES = 'CUSTOMERS_ACTIVES'

class Budget(ModelBase, db.Model):
    month = db.Column(db.Integer(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    value = db.Column(db.DECIMAL(asdecimal=False, precision=17, scale=2), nullable=False)
    ref = db.Column(db.String(256), nullable=False)
    type_ref = db.Column(db.Enum(*[e.value for e in TypeRef]), nullable=False)
    

event.listen(Budget, 'before_insert', input_audit_data_on_insert)
event.listen(Budget, 'before_update', input_audit_data_on_update)