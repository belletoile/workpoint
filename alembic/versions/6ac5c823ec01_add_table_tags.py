"""Add table Tags

Revision ID: 6ac5c823ec01
Revises: 4e249d0ca423
Create Date: 2023-04-24 19:38:51.464397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ac5c823ec01'
down_revision = '4e249d0ca423'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('name', sa.String(), nullable=True))
    op.drop_column('tags', 'title')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('tags', 'name')
    # ### end Alembic commands ###
