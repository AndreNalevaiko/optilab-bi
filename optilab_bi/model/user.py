from enum import Enum
from sqlalchemy import event

from .base import ModelBase
from optilab_bi import db
from optilab_bi.helpers import input_audit_data_on_insert, input_audit_data_on_update

class UserType(Enum):
    """
    Indica o tipo do usuário.
    """
    Admin = 'Admin'
    Operator = 'Operator'

class User(ModelBase, db.Model):
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256))
    active = db.Column(db.Boolean())
    type = db.Column(db.Enum(*[e.value for e in UserType]), nullable=True)

    def __str__(self):
        return '%s' % self.email
    

event.listen(User, 'before_insert', input_audit_data_on_insert)
event.listen(User, 'before_update', input_audit_data_on_update)