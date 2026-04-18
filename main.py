import uvicorn
from dotenv import load_dotenv

from logger_configuration import set_logger

if __name__ == "__main__":
    load_dotenv(override=True)
    set_logger()
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
