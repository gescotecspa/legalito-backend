"""Add clients and case relation

Revision ID: 5f2f70a1c9d0
Revises: 1b52f91b47e5
Create Date: 2026-07-24 22:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '5f2f70a1c9d0'
down_revision = '1b52f91b47e5'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table('clients'):
        op.create_table(
            'clients',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('owner_user', sa.String(length=150), nullable=False),
            sa.Column('name', sa.String(length=255), nullable=False),
            sa.Column('identification', sa.String(length=50), nullable=True),
            sa.Column('email', sa.String(length=150), nullable=True),
            sa.Column('phone_number', sa.String(length=20), nullable=True),
            sa.Column('address', sa.String(length=255), nullable=True),
            sa.Column('notes', sa.Text(), nullable=True),
            sa.Column('status', sa.String(length=50), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['owner_user'], ['users.user']),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index(op.f('ix_clients_owner_user'), 'clients', ['owner_user'], unique=False)

    case_columns = {column['name'] for column in inspector.get_columns('cases')}
    with op.batch_alter_table('cases', schema=None) as batch_op:
        if 'client_id' not in case_columns:
            batch_op.add_column(sa.Column('client_id', sa.Integer(), nullable=True))
            batch_op.create_foreign_key(None, 'clients', ['client_id'], ['id'])


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    case_columns = {column['name'] for column in inspector.get_columns('cases')}
    with op.batch_alter_table('cases', schema=None) as batch_op:
        if 'client_id' in case_columns:
            batch_op.drop_constraint(None, type_='foreignkey')
            batch_op.drop_column('client_id')

    if inspector.has_table('clients'):
        op.drop_index(op.f('ix_clients_owner_user'), table_name='clients')
        op.drop_table('clients')
