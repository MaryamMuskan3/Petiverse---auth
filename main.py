from fastapi import FastAPI
from Authentication.auth import router

app = FastAPI()
app.include_router(router, prefix="/auth")

@app.get("/")
def home():
    return {"Welcome to Petiverse"}