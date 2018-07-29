"""tabela customers

Revision ID: 90e452e6b37c
Revises: 72501f7b87cd
Create Date: 2018-07-28 23:58:57.651827

"""

from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90e452e6b37c'
down_revision = '72501f7b87cd'


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()


def schema_upgrades():
    op.create_table('customer_billing_report',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('customer_code', sa.Integer(), nullable=False),
                    sa.Column('customer_name', sa.String(length=128), nullable=False),
                    sa.Column('business_code', sa.Integer(), nullable=False),
                    sa.Column('current_value', sa.DECIMAL(precision=17, scale=2), nullable=False),
                    sa.Column('latest_value', sa.DECIMAL(precision=17, scale=2), nullable=False),
                    sa.Column('variation', sa.DECIMAL(precision=17, scale=2), nullable=False),
                    sa.Column('month', sa.Integer(), nullable=False),
                    sa.Column('year', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime, nullable=False),
                    sa.Column('updated_at', sa.DateTime, nullable=True))

    op.create_table('number_active_customers',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('average_latest_year', sa.DECIMAL(precision=17, scale=2), nullable=False),
                    sa.Column('number_current_day', sa.Integer(), nullable=False),
                    sa.Column('number_current_month', sa.Integer(), nullable=False),
                    sa.Column('number_latest_day', sa.Integer(), nullable=False),
                    sa.Column('number_latest_month', sa.Integer(), nullable=False),
                    sa.Column('business_code', sa.Integer(), nullable=False),
                    sa.Column('date', sa.Date, nullable=False),
                    sa.Column('created_at', sa.DateTime, nullable=False),
                    sa.Column('updated_at', sa.DateTime, nullable=True))

def schema_downgrades():
    op.drop_table('customer_billing_report')
    op.drop_table('number_active_customers')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
