import sqlalchemy as sa
from sqlalchemy import (
    Table as TB,
    Boolean, Column, ForeignKey, Integer, String,
)
#
from apps.sql.config import Base, metadata


##############################################################
class IPS(Base):
    __tablename__ = "ips"
    #
    id = Column(Integer, primary_key=True, autoincrement=True)
    #
    ip = Column(String, unique=True, nullable=False)
    port = Column(String, nullable=False)
    now = Column(String, nullable=False)
    goodcnt = Column(Integer, nullable=False)


# 從Alembic的upgrade複製過來修改
tb_ips = TB('ips',
            metadata,  # 加這個
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('ip', sa.String(), nullable=False),
            sa.Column('port', sa.String(), nullable=False),
            sa.Column('now', sa.String(), nullable=False),
            sa.Column('goodcnt', sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('ip')
            )
