"""Data no report products e customers

Revision ID: 120ea54fb16f
Revises: 8aef47536386
Create Date: 2019-01-14 10:45:24.902408

"""

from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '120ea54fb16f'
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
    op.add_column('report_products', sa.Column('date', sa.Date()))
    op.add_column('customer_billing_report', sa.Column('date', sa.Date()))


def schema_downgrades():
    op.drop_column('report_products', 'date')
    op.drop_column('customer_billing_report', 'date')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
