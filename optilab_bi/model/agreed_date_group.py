
from sqlalchemy import event

from .base import ModelBase
from optilab_bi import db
from optilab_bi.helpers import input_audit_data_on_insert, input_audit_data_on_update


class AgreedDateGroup(ModelBase, db.Model):
    date = db.Column(db.JSON(), nullable=False)
    business_code = db.Column(db.Integer(), nullable=False)


event.listen(AgreedDateGroup, 'before_insert', input_audit_data_on_insert)
event.listen(AgreedDateGroup, 'before_update', input_audit_data_on_update)