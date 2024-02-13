"""height

Revision ID: 539b002caa8d
Revises: f96efcd87edc
Create Date: 2024-02-12 14:18:10.713208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '539b002caa8d'
down_revision = 'f96efcd87edc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('height', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('height')

    # ### end Alembic commands ###
