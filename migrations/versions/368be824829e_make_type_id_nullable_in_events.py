"""Make type_id nullable in events

Revision ID: 368be824829e
Revises: e7889835b314
Create Date: 2025-04-10 17:29:42.870534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '368be824829e'
down_revision = 'e7889835b314'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.alter_column('type_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.alter_column('type_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
