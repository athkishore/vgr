"""empty message

Revision ID: 3e9a465edc4d
Revises: 867adbff51e
Create Date: 2016-02-11 10:06:08.914167

"""

# revision identifiers, used by Alembic.
revision = '3e9a465edc4d'
down_revision = '867adbff51e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('category_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'category_id')
    ### end Alembic commands ###