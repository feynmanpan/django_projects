import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
import databases
####################################################


# 由main的startup啟動連線 # await dbwtb.connect()
DB_URL = "postgresql://pan:pgcode@localhost/wtb"
# 三個提供給外部使用
dbwtb = databases.Database(DB_URL, ssl=False)
metadata = sa.MetaData()
Base = declarative_base()
