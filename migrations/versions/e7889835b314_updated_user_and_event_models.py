"""Updated User and Event models

Revision ID: e7889835b314
Revises: 0bb56e93c8ba
Create Date: 2025-04-10 17:25:08.736763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7889835b314'
down_revision = '0bb56e93c8ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_date', sa.DateTime(), nullable=False))
        batch_op.create_foreign_key(None, 'users', ['user'], ['user'])
        batch_op.create_foreign_key(None, 'parameters', ['type_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('start_date')

    # ### end Alembic commands ###
