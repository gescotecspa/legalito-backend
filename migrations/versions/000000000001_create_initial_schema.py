"""Create initial schema

Revision ID: 000000000001
Revises:
Create Date: 2026-05-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '000000000001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    def create_table_if_missing(name, *columns, **kwargs):
        if not inspector.has_table(name):
            op.create_table(name, *columns, **kwargs)

    create_table_if_missing(
        'assistants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('phone_number', sa.String(length=20), nullable=True),
        sa.Column('type_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('image_url', sa.String(length=250), nullable=True),
        sa.Column('region_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    create_table_if_missing(
        'cases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('rit', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('rit'),
    )

    create_table_if_missing(
        'courthouses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('type_id', sa.Integer(), nullable=True),
        sa.Column('address', sa.String(length=250), nullable=False),
        sa.Column('phone_number', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('website', sa.String(length=150), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    create_table_if_missing(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('folio_id', sa.Integer(), nullable=True),
        sa.Column('rit', sa.String(length=100), nullable=True),
        sa.Column('subject', sa.String(length=255), nullable=False),
        sa.Column('sender', sa.String(length=255), nullable=False),
        sa.Column('received_date', sa.DateTime(), nullable=False),
        sa.Column('body', sa.Text(), nullable=True),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.Column('marked_as_invitation', sa.Boolean(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('user', sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    create_table_if_missing(
        'parameters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    create_table_if_missing(
        'roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    create_table_if_missing(
        'terms_and_conditions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('version', sa.String(length=10), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    create_table_if_missing(
        'users',
        sa.Column('user', sa.String(length=150), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('phone_number', sa.String(length=20), nullable=True),
        sa.Column('birth_date', sa.DateTime(), nullable=True),
        sa.Column('image_url', sa.String(length=200), nullable=True),
        sa.Column('activation_date', sa.DateTime(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('suspended_at', sa.DateTime(), nullable=True),
        sa.Column('suspension_reason', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint('user'),
    )

    create_table_if_missing(
        'cases_users',
        sa.Column('case_id', sa.Integer(), nullable=False),
        sa.Column('user', sa.String(length=150), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id']),
        sa.ForeignKeyConstraint(['user'], ['users.user']),
        sa.PrimaryKeyConstraint('case_id', 'user'),
    )

    create_table_if_missing(
        'email_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('imap_server', sa.String(length=100), nullable=False),
        sa.Column('email_address', sa.String(length=150), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('user', sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email_address'),
    )

    create_table_if_missing(
        'events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type_id', sa.Integer(), nullable=False),
        sa.Column('user', sa.String(length=150), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    create_table_if_missing(
        'favorites',
        sa.Column('assistant_id', sa.Integer(), nullable=False),
        sa.Column('user', sa.String(length=150), nullable=False),
        sa.ForeignKeyConstraint(['assistant_id'], ['assistants.id']),
        sa.ForeignKeyConstraint(['user'], ['users.user']),
        sa.PrimaryKeyConstraint('assistant_id', 'user'),
    )

    create_table_if_missing(
        'folios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), nullable=False),
        sa.Column('folio_number', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('folios')
    op.drop_table('favorites')
    op.drop_table('events')
    op.drop_table('email_accounts')
    op.drop_table('cases_users')
    op.drop_table('users')
    op.drop_table('terms_and_conditions')
    op.drop_table('roles')
    op.drop_table('parameters')
    op.drop_table('notifications')
    op.drop_table('courthouses')
    op.drop_table('cases')
    op.drop_table('assistants')
