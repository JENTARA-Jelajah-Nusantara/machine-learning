from fastapi import APIRouter, Query
from typing import List
import numpy as np
import requests
from app.models import PlacesData, Place, Review, Text, AuthorAttribution, Location, DisplayName, Photo
from app.config import model
from app.preprocessing import prep_pred

router = APIRouter()

@router.get("/get-travel-spots-and-predict")
async def get_travel_spots_and_predict(
    includedTypes: List[str] = Query(...,
                                     description="Kategori tempat wisata"),
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
    radius: int = Query(..., description="Radius dalam meters"),
    limit: int = Query(3, description="Limit output tempat wisata")
):
    url = "https://places.googleapis.com/v1/places:searchNearby"

    payload = {
        "includedTypes": includedTypes,
        "maxResultCount": 15,
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
        "X-Goog-Api-Key": "Masukkan Key API Anda Disini",
        "X-Goog-FieldMask": "places.displayName,places.reviews,places.location,places.formattedAddress,places.photos"
    }

    response = requests.post(url, json=payload, headers=headers)
    travel_spots = response.json()

    if 'places' not in travel_spots:
        return {"No Places Found"}

    res = []
    for place in travel_spots['places']:
        reviews = place.get('reviews', [])
        review_sentiments = []
        processed_reviews = []

        for review in reviews:
            text = review.get('text', {}).get('text')
            sentiment = None
            if text:
                sentiment = int(np.argmax(model.predict(prep_pred(text))[0])) + 1
                review_sentiments.append(sentiment)

            processed_reviews.append({
                'name': review.get('name'),
                'relativePublishTimeDescription': review.get('relativePublishTimeDescription'),
                'rating': review.get('rating'),
                'text': review.get('text'),
                'originalText': review.get('originalText'),
                'authorAttribution': review.get('authorAttribution'),
                'publishTime': review.get('publishTime'),
                'sentiment': sentiment
            })

        average_sentiment = sum(review_sentiments) / len(review_sentiments) if review_sentiments else None

        res.append({
            'formattedAddress': place.get('formattedAddress'),
            'location': place.get('location'),
            'displayName': place.get('displayName'),
            'reviews': processed_reviews,
            'photos': place.get('photos'),
            'averageSentiment': average_sentiment
        })

    sorted_res = sorted(res, key=lambda x: x['averageSentiment'], reverse=True)
    limited_res = sorted_res[:limit]

    return limited_res