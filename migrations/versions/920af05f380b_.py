"""empty message

Revision ID: 920af05f380b
Revises: 011dfde256a4
Create Date: 2020-04-21 20:40:49.676067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '920af05f380b'
down_revision = '011dfde256a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ViewPoint', sa.Column('image', sa.String(), nullable=True))
    op.drop_column('ViewPoint', 'image_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ViewPoint', sa.Column('image_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('ViewPoint', 'image')
    # ### end Alembic commands ###