"""tabela KPI

Revision ID: 1602b38797b9
Revises: 90e452e6b37c
Create Date: 2018-07-31 23:13:51.972980

"""

from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1602b38797b9'
down_revision = '90e452e6b37c'


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()


def schema_upgrades():
    op.create_table('kpi',
                sa.Column('id', sa.Integer, nullable=False),
                sa.PrimaryKeyConstraint('id'),
                sa.Column('average_billing', sa.DECIMAL(precision=17, scale=2), nullable=False),
                sa.Column('average_order_quantity', sa.DECIMAL(precision=17, scale=2), nullable=False),
                sa.Column('average_tm', sa.DECIMAL(precision=17, scale=2), nullable=False),
                sa.Column('average_quantity_pieces', sa.DECIMAL(precision=17, scale=2), nullable=False),
                sa.Column('last_day_billing', sa.DECIMAL(precision=17, scale=2), nullable=True),
                sa.Column('last_day_order_quantity', sa.DECIMAL(precision=17, scale=2), nullable=True),
                sa.Column('last_day_tm', sa.DECIMAL(precision=17, scale=2), nullable=True),
                sa.Column('last_day_quantity_pieces', sa.DECIMAL(precision=17, scale=2), nullable=True),
                sa.Column('budget_billing', sa.DECIMAL(precision=17, scale=2), nullable=True),
                sa.Column('budget_order_quantity', sa.DECIMAL(precision=17, scale=2), nullable=True),
                sa.Column('budget_tm', sa.DECIMAL(precision=17, scale=2), nullable=True),
                sa.Column('budget_quantity_pieces', sa.DECIMAL(precision=17, scale=2), nullable=True),
                sa.Column('month', sa.Integer(), nullable=False),
                sa.Column('year', sa.Integer(), nullable=False),
                sa.Column('business_code', sa.Integer(), nullable=False),
                sa.Column('date', sa.DateTime, nullable=False),
                sa.Column('created_at', sa.DateTime, nullable=False),
                sa.Column('updated_at', sa.DateTime, nullable=True))


def schema_downgrades():
    op.drop_table('kpi')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
