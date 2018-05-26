"""products

Revision ID: 72501f7b87cd
Revises: 16e0c5a4ca16
Create Date: 2018-05-07 23:44:18.682888

"""

from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72501f7b87cd'
down_revision = '16e0c5a4ca16'


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()


def schema_upgrades():
    op.create_table('product',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('label', sa.String(length=64), nullable=False), sa.UniqueConstraint('label'),
                    sa.Column('like_or', sa.String(length=256), nullable=True),
                    sa.Column('like_and', sa.String(length=256), nullable=True),
                    sa.Column('color', sa.Integer(), nullable=True),
                    sa.Column('process', sa.String(length=32), nullable=True),
                    sa.Column('type', sa.String(length=32), nullable=True),
                    sa.Column('show_in_abstract', sa.String(length=32), nullable=False),
                    sa.Column('created_at', sa.DateTime, nullable=False),
                    sa.Column('updated_at', sa.DateTime, nullable=True))
                    
    op.create_table('report_products',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('brand', sa.String(length=128), nullable=False),
                    sa.Column('label', sa.String(length=128), nullable=False),
                    sa.Column('status', sa.Enum('OPENED', 'CLOSED'), nullable=False),
                    sa.Column('business_code', sa.Integer(), nullable=False),
                    sa.Column('month', sa.Integer(), nullable=False),
                    sa.Column('latest_year', sa.Integer(), nullable=False),
                    sa.Column('current_year', sa.Integer(), nullable=False),
                    sa.Column('qtd_latest_year', sa.Integer(), nullable=False),
                    sa.Column('value_latest_year', sa.DECIMAL(precision=17, scale=2), nullable=False),
                    sa.Column('qtd_current_year', sa.Integer(), nullable=False),
                    sa.Column('value_current_year', sa.DECIMAL(precision=17, scale=2), nullable=False),
                    sa.Column('created_at', sa.DateTime, nullable=False),
                    sa.Column('updated_at', sa.DateTime, nullable=True))

def schema_downgrades():
    op.drop_table('product')
    op.drop_table('report_products')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
