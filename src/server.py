from dotenv import load_dotenv
from fastapi import FastAPI

from logger_configuration import set_logger
from src.modules import register_modules

load_dotenv(override=True)
set_logger()

app = FastAPI(title="EGE Cards API", version="0.1a")
register_modules(app)


@app.get("/")
def root():
    return {"server": "running"}
