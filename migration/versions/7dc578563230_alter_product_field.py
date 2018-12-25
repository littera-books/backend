"""alter product field

Revision ID: 7dc578563230
Revises: 61159a79914c
Create Date: 2018-12-25 11:16:21.155627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dc578563230'
down_revision = '61159a79914c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('product', sa.Column('books', sa.Integer(), unique=False, nullable=False, default=0))

    op.execute("""
        UPDATE product
        SET books = 0
    """)


def downgrade():
    op.drop_column('product', 'books')
