"""change log column

Revision ID: 0fdafb9bbb12
Revises: a2344923d302
Create Date: 2019-09-01 15:36:14.742629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fdafb9bbb12'
down_revision = 'a2344923d302'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('littera_user', sa.Column('log', sa.String(), server_default="created_user", nullable=False))
    op.add_column('subscription', sa.Column('log', sa.String(), server_default="add_subscription", nullable=False))


def downgrade():
    op.drop_column('littera_user', 'log')
    op.drop_column('message', 'log')
    op.drop_column('subscription', 'log')
