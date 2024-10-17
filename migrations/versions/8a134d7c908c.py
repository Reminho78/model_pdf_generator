"""Create form table

Revision ID: 8a134d7c908c
Revises: 
Create Date: 2024-10-17 15:30:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a134d7c908c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Créer la table 'form'
    op.create_table(
        'form',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('implantation', sa.String(length=120), nullable=False),
        sa.Column('creation_date', sa.Date(), nullable=False),
        sa.Column('billing_address', sa.String(length=250), nullable=False),
        sa.Column('shipping_address', sa.String(length=250), nullable=False),
        sa.Column('reason', sa.String(length=250), nullable=False),
        sa.Column('other_reason', sa.String(length=250), nullable=True)
    )


def downgrade():
    # Supprimer la table 'form'
    op.drop_table('form')