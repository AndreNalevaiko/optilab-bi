"""Ajuste model Budget

Revision ID: 0e8a33f4561b
Revises: 0d72506c01b7
Create Date: 2019-09-21 15:36:46.591060

"""

from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e8a33f4561b'
down_revision = '0d72506c01b7'


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()


def schema_upgrades():
    op.alter_column('budget', 'business_code', new_column_name='ref', type_=sa.String(256), nullable=True)
    op.add_column('budget', sa.Column('type_ref', sa.Enum('BILLING', 'PRODUCT_VALUE', 'PRODUCT_AMOUNT', 'CUSTOMERS_ACTIVES'), nullable=False, server_default='BILLING'))


def schema_downgrades():
    op.alter_column('budget', 'ref', new_column_name='business_code', type_=sa.String(256), nullable=True)
    op.drop_column('budget', 'type_ref')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
