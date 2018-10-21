"""agreed date group

Revision ID: 7e2dddcc2cb2
Revises: 1602b38797b9
Create Date: 2018-10-20 21:15:22.317014

"""

from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e2dddcc2cb2'
down_revision = '1602b38797b9'


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()


def schema_upgrades():
    op.create_table('agreed_date_group',
                sa.Column('id', sa.Integer, nullable=False),
                sa.PrimaryKeyConstraint('id'),
                sa.Column('date', sa.JSON(), nullable=False),
                sa.Column('business_code', sa.Integer(), nullable=False),
                sa.Column('created_at', sa.DateTime, nullable=False),
                sa.Column('updated_at', sa.DateTime, nullable=True))


def schema_downgrades():
    op.drop_table('agreed_date_group')

def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
