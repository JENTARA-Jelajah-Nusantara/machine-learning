from fastapi import APIRouter, Query
from typing import List
import requests

router = APIRouter()


@router.get("/get-travel-spots")
async def get_travel_spots(
    includedTypes: List[str] = Query(...,
                                     description="Kategori tempat wisata"),
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
    radius: int = Query(..., description="Radius dalam meters")
):
    url = "https://places.googleapis.com/v1/places:searchNearby"

    payload = {
        "includedTypes": includedTypes,
        "maxResultCount": 5,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": radius
            }
        },
        "languageCode": "id"
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": "Masukkan API Key di sini",
        "X-Goog-FieldMask": "places.displayName,places.reviews,places.location,places.formattedAddress,places.photos"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
