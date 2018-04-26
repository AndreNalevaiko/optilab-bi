from datetime import datetime


def input_audit_data_on_insert(mapper, connection, target):
    """Atualiza a data de criação (create_at) na inclusão da entidade."""

    if hasattr(target, 'created_at'):
        target.created_at = datetime.utcnow()


def input_audit_data_on_update(mapper, connection, target):
    """Atualiza a data de atualização (create_at) na alteração da entidade."""

    if hasattr(target, 'updated_at'):
        target.updated_at = datetime.utcnow()

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, DateTime

