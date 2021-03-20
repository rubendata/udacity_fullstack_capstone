"""empty message

Revision ID: 1fb956812abe
Revises: 016e4a98a63a
Create Date: 2021-03-10 07:50:37.127688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fb956812abe'
down_revision = '016e4a98a63a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('comment', sa.String(), nullable=False))
    op.drop_column('posts', 'content')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('content', sa.VARCHAR(length=8000), autoincrement=False, nullable=False))
    op.drop_column('posts', 'comment')
    # ### end Alembic commands ###