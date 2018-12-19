"""alter user field

Revision ID: 61159a79914c
Revises: 
Create Date: 2018-12-19 22:40:25.012561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61159a79914c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('littera_user', 'first_name', nullable=True),
    op.alter_column('littera_user', 'last_name', nullable=True),
    op.alter_column('littera_user', 'address', nullable=True),
    op.alter_column('littera_user', 'phone', nullable=True),


def downgrade():
    op.alter_column('littera_user', 'first_name', nullable=False),
    op.alter_column('littera_user', 'last_name', nullable=False),
    op.alter_column('littera_user', 'address', nullable=False),
    op.alter_column('littera_user', 'phone', nullable=False),
