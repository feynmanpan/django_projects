from fastapi import FastAPI
from typing import Optional, Callable
from views_5002 import test
#


app = FastAPI()


def path_get(url: str, func: Callable):
    return app.get(url)(func)


# urlpattern
path_get("/", test)
