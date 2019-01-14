"""users_roles

Revision ID: 8aef47536386
Revises: 7e2dddcc2cb2
Create Date: 2018-12-19 23:41:57.314598

"""

from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8aef47536386'
down_revision = '7e2dddcc2cb2'


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()


def schema_upgrades():
    op.drop_table('user')

    op.create_table('file',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('file_name', sa.String(length=512), nullable=False),
                    sa.Column('url', sa.String(length=512), nullable=False),
                    sa.Column('content_type', sa.String(length=256), nullable=False),
                    sa.Column('size', sa.Integer(), nullable=False),
                    sa.Column('height', sa.Integer(), nullable=True),
                    sa.Column('width', sa.Integer(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False))

    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('email', sa.String(length=256), nullable=False),
                    sa.UniqueConstraint('email'),
                    sa.Column('name', sa.String(length=256), nullable=False),
                    sa.Column('password', sa.String(length=256), nullable=True),
                    sa.Column('profile_photo_id', sa.Integer()),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
                    sa.Column('last_login_at', sa.DateTime(), nullable=True),
                    sa.Column('current_login_at', sa.DateTime(), nullable=True),
                    sa.Column('last_login_ip', sa.String(length=256), nullable=True),
                    sa.Column('current_login_ip', sa.String(length=256), nullable=True),
                    sa.Column('login_count', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('last_user_agent', sa.String(1024)),
                    sa.Column('current_user_agent', sa.String(1024)),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['profile_photo_id'], ['file.id'], name='fk_user_profile_photo_id_file'),
    )

    op.create_table('role',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=256), nullable=False),
                    sa.Column('access', sa.String(length=4000), nullable=True),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('roles_users',
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('role_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id']))

def schema_downgrades():
    op.drop_table('roles_users')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('file')


def data_upgrades():
    op.execute("""
        INSERT INTO `optilab-bi`.`user` (`email`, `name`, `password`, `active`, `created_at`, `updated_at`) \n
        VALUES ('andre@gorillascode.com', 'Andre Nalevaiko', '123456', '1','2018-05-12 00:01:00', '2018-05-12 00:01:00')
    """)

    op.execute("""
        INSERT INTO `optilab-bi`.`user` (`email`, `name`, `password`, `active`, `created_at`, `updated_at`)
        VALUES ('mariana@laboptilab.com', 'Mariana Rossoni', 'itop654', '1','2018-05-12 00:01:00', '2018-05-12 00:01:00')
    """)

    op.execute("""
        INSERT INTO `optilab-bi`.`role` (`name`) VALUES ('admin');
        INSERT INTO `optilab-bi`.`role` (`name`, `access`) VALUES ('viewer', 'billing,products,customers,rate_service')
    """)

    op.execute("INSERT into `optilab-bi`.roles_users VALUES (1,1), (2,1)")


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
