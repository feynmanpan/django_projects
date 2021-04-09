import asyncio
#
# import sqlalchemy as sa
########################################################


async def single_insert(db, tb, row):
    query = tb.insert().values(**row)
    await db.execute(query)


async def bulk_insert(db, tb, rows):
    await db.execute(tb.delete())
    tasks = [asyncio.create_task(single_insert(db, tb, r)) for r in rows]
    await asyncio.wait(tasks)
