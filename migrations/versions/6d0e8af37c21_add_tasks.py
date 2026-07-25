"""Add tasks

Revision ID: 6d0e8af37c21
Revises: 5f2f70a1c9d0
Create Date: 2026-07-24 23:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '6d0e8af37c21'
down_revision = '5f2f70a1c9d0'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table('tasks'):
        op.create_table(
            'tasks',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('owner_user', sa.String(length=150), nullable=False),
            sa.Column('title', sa.String(length=255), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('status', sa.String(length=50), nullable=False),
            sa.Column('priority', sa.String(length=50), nullable=False),
            sa.Column('due_date', sa.DateTime(), nullable=True),
            sa.Column('assignee_user', sa.String(length=150), nullable=True),
            sa.Column('case_id', sa.Integer(), nullable=True),
            sa.Column('client_id', sa.Integer(), nullable=True),
            sa.Column('completed_at', sa.DateTime(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['case_id'], ['cases.id']),
            sa.ForeignKeyConstraint(['client_id'], ['clients.id']),
            sa.ForeignKeyConstraint(['owner_user'], ['users.user']),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index(op.f('ix_tasks_owner_user'), 'tasks', ['owner_user'], unique=False)
        op.create_index(op.f('ix_tasks_case_id'), 'tasks', ['case_id'], unique=False)
        op.create_index(op.f('ix_tasks_client_id'), 'tasks', ['client_id'], unique=False)


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if inspector.has_table('tasks'):
        op.drop_index(op.f('ix_tasks_client_id'), table_name='tasks')
        op.drop_index(op.f('ix_tasks_case_id'), table_name='tasks')
        op.drop_index(op.f('ix_tasks_owner_user'), table_name='tasks')
        op.drop_table('tasks')
