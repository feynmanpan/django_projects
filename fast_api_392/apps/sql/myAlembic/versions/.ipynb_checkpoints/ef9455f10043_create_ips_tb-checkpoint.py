"""create ips tb

Revision ID: ef9455f10043
Revises: 
Create Date: 2021-04-08 19:40:19.365349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef9455f10043'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ips',
    sa.Column('ip', sa.String(), nullable=False),
    sa.Column('port', sa.String(), nullable=False),
    sa.Column('now', sa.String(), nullable=False),
    sa.Column('goodcnt', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('ip')
    )
#     op.drop_table('fruits')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
#     op.create_table('fruits',
#     sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
#     sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
#     sa.PrimaryKeyConstraint('id', name='fruits_pkey')
#     )
    op.drop_table('ips')
    # ### end Alembic commands ###
