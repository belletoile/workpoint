"""change reviews

Revision ID: a3db713145f1
Revises: 2ad87a5c2268
Create Date: 2023-06-02 11:52:43.064955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3db713145f1'
down_revision = '2ad87a5c2268'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('user_name', sa.String(), nullable=True))
    op.add_column('reviews', sa.Column('user_surname', sa.String(), nullable=True))
    op.add_column('reviews', sa.Column('user_photo', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reviews', 'user_photo')
    op.drop_column('reviews', 'user_surname')
    op.drop_column('reviews', 'user_name')
    # ### end Alembic commands ###