"""Ajout de la colonne pdf_generated dans Form

Revision ID: 6a8e0ec381a7
Revises: 0274920a0da2
Create Date: 2024-10-18 04:08:55.053601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a8e0ec381a7'
down_revision = '0274920a0da2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('form', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pdf_generated', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('form', schema=None) as batch_op:
        batch_op.drop_column('pdf_generated')

    # ### end Alembic commands ###
