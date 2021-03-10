from fastapi import FastAPI
#


app = FastAPI()
#


@app.get("/")
def pig():
    return 123
