"""add info field in subscription

Revision ID: 34ac39624027
Revises: 09c623fd23e7
Create Date: 2018-12-28 00:48:05.135333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34ac39624027'
down_revision = '09c623fd23e7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('subscription', sa.Column('first_name', sa.String(20), unique=False, nullable=True))
    op.add_column('subscription', sa.Column('last_name', sa.String(20), unique=False, nullable=True))
    op.add_column('subscription', sa.Column('address', sa.String(), unique=False, nullable=True))
    op.add_column('subscription', sa.Column('phone', sa.String(20), unique=True, nullable=True))


def downgrade():
    op.drop_column('subscription', 'first_name')
    op.drop_column('subscription', 'last_name')
    op.drop_column('subscription', 'address')
    op.drop_column('subscription', 'phone')
