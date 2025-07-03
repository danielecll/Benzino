from fastapi import FastAPI
from contextlib import asynccontextmanager
from schemas import GeoData
from services.query import locate_stations
from services.data_loader import load_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_data()
    print("Listening...")
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/locate")
def locate(rdata: GeoData):
    return locate_stations(rdata)