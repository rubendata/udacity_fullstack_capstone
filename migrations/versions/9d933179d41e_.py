"""empty message

Revision ID: 9d933179d41e
Revises: 9799cf2eb5e9
Create Date: 2021-03-19 21:24:54.629921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d933179d41e'
down_revision = '9799cf2eb5e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'group_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'group_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
