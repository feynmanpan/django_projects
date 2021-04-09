import sqlalchemy
from sqlalchemy import (
    Table as TB,
    Column as COL,
    Integer as INT,
    String as STR,
)
import databases
import pandas as pd
####################################################

DB_URL = "postgresql://pan:pgcode@localhost/wtb"
dbwtb = databases.Database(DB_URL, ssl=False)
metadata = sqlalchemy.MetaData()


# 由main的startup啟動連線
# await pgwtb.connect()
