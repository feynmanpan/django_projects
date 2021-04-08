"""create ips table

Revision ID: df6f5c8314fc
Revises: 
Create Date: 2021-04-08 16:22:40.272292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df6f5c8314fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ips',
        sa.Column('ip', sa.String, primary_key=True),
        sa.Column('port', sa.String, nullable=False),
        sa.Column('now', sa.String, nullable=False),
        sa.Column('goodcnt', sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('ips')
