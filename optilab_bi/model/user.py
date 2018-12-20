from enum import Enum
from sqlalchemy import event
from gorillaspy.business.model import ModelBase, File
from optilab_bi import db
from optilab_bi.helpers import input_audit_data_on_insert, input_audit_data_on_update
from flask_security.core import UserMixin, RoleMixin

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(ModelBase, db.Model, UserMixin):
    id = db.Column(db.Integer(), nullable=False, primary_key=True)

    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(256))
    current_login_ip = db.Column(db.String(256))
    login_count = db.Column(db.Integer)
    last_user_agent = db.Column(db.String(1024))
    current_user_agent = db.Column(db.String(1024))

    profile_photo_id = db.Column(db.Integer, db.ForeignKey(File.id))
    profile_photo = db.relationship(File, foreign_keys=profile_photo_id)

    roles = db.relationship('Role', secondary=roles_users)

    def __str__(self):
        return '%s' % self.email


class Role(db.Model, RoleMixin):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    access = db.Column(db.String(4000))

    users = db.relationship('User', secondary='roles_users')

    def __str__(self):
        return '%s' % self.name
    

event.listen(User, 'before_insert', input_audit_data_on_insert)
event.listen(User, 'before_update', input_audit_data_on_update)