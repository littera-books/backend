"""add thumbnail field in product

Revision ID: 09c623fd23e7
Revises: 7dc578563230
Create Date: 2018-12-26 12:27:48.340197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09c623fd23e7'
down_revision = '7dc578563230'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('product', sa.Column('thumbnail_url', sa.String(), unique=False, nullable=True))


def downgrade():
    op.drop_column('product', 'thumbnail_url')
