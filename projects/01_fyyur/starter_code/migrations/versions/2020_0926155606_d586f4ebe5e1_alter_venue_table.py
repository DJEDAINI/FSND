"""Alter Venue Table

Revision ID: d586f4ebe5e1
Revises: 6ec55e0eb555
Create Date: 2020-09-26 15:56:06.938727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd586f4ebe5e1'
down_revision = '6ec55e0eb555'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', sa.ARRAY(sa.String(120), dimensions=1), nullable=True))
    op.add_column('Venue', sa.Column('seeking_description', sa.Text(), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('website', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'website')
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###
