from pydantic import BaseModel

class GeoData(BaseModel):
    lat: float
    lon: float
    radius: float
    fuel: str