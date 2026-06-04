from fastapi import FastAPI
from utils.logger import *
from utils.init import initialize
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from time import sleep
from _thread import *
from routes.rack_device_details import router as rack_device_details_router
import os


app = FastAPI(
    title="RealCount API"
)


@app.on_event("startup")
async def init_processes():
    logging.info("Started main")
    log_path = os.environ.get("LOG_PATH", os.getcwd() + '/log')
    os.environ['LOG_PATH'] = log_path
    initialize(log_path)
    logging.info("Now initializing env variables")


app.include_router(rack_device_details_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=14001, reload=False)

