from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, DateTime

__author__ = 'andré'


Table = declarative_base()


class ModelBase(object):
    """ Auditable
    Classe que define colunas utilizadas em todas as tabelas e em auditorias nos registros da base.
    """

    id = Column(Integer, primary_key=True, autoincrement=True)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

    def __repr__(self):
        return "%s.%s(id=%r)" % (self.__class__.__module__, self.__class__.__name__, self.id)

    def __str__(self):
        return "%s" % self.id or 'new object'