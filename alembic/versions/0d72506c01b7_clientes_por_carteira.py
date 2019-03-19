"""Clientes por carteira

Revision ID: 0d72506c01b7
Revises: 8aef47536386
Create Date: 2019-03-16 15:13:30.574914

"""

from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d72506c01b7'
down_revision = '8aef47536386'


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()


def schema_upgrades():
    op.add_column('customer_billing_report', sa.Column('seller', sa.Integer(), nullable=False))
    op.add_column('number_active_customers', sa.Column('seller', sa.Integer(), nullable=False))
    op.add_column('report_products', sa.Column('seller', sa.Integer(), nullable=False))

    op.drop_column('customer_billing_report', 'business_code')
    op.drop_column('number_active_customers', 'business_code')
    op.drop_column('report_products', 'business_code')


def schema_downgrades():
    op.drop_column('customer_billing_report', 'seller')
    op.drop_column('number_active_customers', 'seller')
    op.drop_column('report_products', 'seller')

    op.add_column('number_active_customers', sa.Column('business_code', sa.Integer(), nullable=False))
    op.add_column('customer_billing_report', sa.Column('business_code', sa.Integer(), nullable=False))
    op.add_column('report_products', sa.Column('business_code', sa.Integer(), nullable=False))

def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
