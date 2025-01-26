from fastapi import FastAPI
from src.mailing import routes


app = FastAPI()
app.include_router(routes.router)
