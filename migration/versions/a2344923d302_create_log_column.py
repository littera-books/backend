"""create log column

Revision ID: a2344923d302
Revises: 
Create Date: 2019-08-30 21:40:15.527956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2344923d302'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('littera_user', sa.Column('log', sa.Boolean(), default=False))
    op.add_column('message', sa.Column('log', sa.Boolean(), default=False))
    op.add_column('subscription', sa.Column('log', sa.Boolean(), default=False))


def downgrade():
    op.drop_column('littera_user', 'log')
    op.drop_column('message', 'log')
    op.drop_column('subscription', 'log')
