from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
# 
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'])

@app.get("/api/")
async def root():
    return {"message": "Hello World!! YES! no nonono"}