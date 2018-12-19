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
    op.alter_column(
        'littera_user',
        sa.Column('first_name', sa.String(20), unique=False, nullable=True),
        sa.Column('last_name', sa.String(20), unique=False, nullable=True),
        sa.Column('address', sa.String, unique=False, nullable=True),
        sa.Column('phone', sa.String(20), unique=True, nullable=True),
    )


def downgrade():
    op.alter_column(
        'littera_user',
        sa.Column('first_name', sa.String(20), unique=False, nullable=False),
        sa.Column('last_name', sa.String(20), unique=False, nullable=False),
        sa.Column('address', sa.String, unique=False, nullable=False),
        sa.Column('phone', sa.String(20), unique=True, nullable=False),
    )
