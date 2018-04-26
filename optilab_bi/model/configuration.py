
from sqlalchemy import event

from .base import ModelBase
from optilab_bi import db
from optilab_bi.helpers import input_audit_data_on_insert, input_audit_data_on_update


class Configuration(ModelBase, db.Model):
    key = db.Column(db.Integer(), nullable=False)
    value = db.Column(db.String(256), nullable=False)


event.listen(Configuration, 'before_insert', input_audit_data_on_insert)
event.listen(Configuration, 'before_update', input_audit_data_on_update)