"""Setup_inicial

Revision ID: 16e0c5a4ca16
Revises: 87ad36f97b44
Create Date: 2018-04-25 21:41:07.593209

"""

from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16e0c5a4ca16'
down_revision = '87ad36f97b44'


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()


def schema_upgrades():
    op.create_table('user',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('name', sa.String(length=64), nullable=False),
                    sa.Column('email', sa.String(length=64), nullable=False),
                    sa.Column('password', sa.String(length=64), nullable=False),
                    sa.Column('type', sa.Enum('Admin', 'Operator'), nullable=False),
                    sa.Column('created_at', sa.DateTime, nullable=False),
                    sa.Column('updated_at', sa.DateTime, nullable=True))

    op.create_table('budget',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('month', sa.Integer(), nullable=False),
                    sa.Column('year', sa.Integer(), nullable=False),
                    sa.Column('business_code', sa.Integer(), nullable=False),
                    sa.Column('value', sa.DECIMAL(precision=17, scale=2), nullable=False),
                    sa.Column('created_at', sa.DateTime, nullable=False),
                    sa.Column('updated_at', sa.DateTime, nullable=True))

    op.create_table('configuration',
                sa.Column('id', sa.Integer, nullable=False),
                sa.PrimaryKeyConstraint('id'),
                sa.Column('key', sa.String(length=256), nullable=False),
                sa.Column('value',sa.String(length=256), nullable=False),
                sa.Column('created_at', sa.DateTime, nullable=False),
                sa.Column('updated_at', sa.DateTime, nullable=True))


def schema_downgrades():
    op.drop_table('configuration')
    op.drop_table('user')
    op.drop_table('budget')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
