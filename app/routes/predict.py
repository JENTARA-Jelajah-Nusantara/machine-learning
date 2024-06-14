from fastapi import APIRouter
import numpy as np
from app.models import PlacesData
from app.config import model
from app.preprocessing import prep_pred

router = APIRouter()

@router.post("/predict/")
async def predict(data: PlacesData, limit: int = 3):
    res = []
    for place in data.places:
        review_sentiments = []
        processed_reviews = []

        for review in place.reviews:
            if review.text and review.text.text:
                sentiment = int(np.argmax(model.predict(prep_pred(review.text.text))[0])) + 1
                review_sentiments.append(sentiment)
            else:
                sentiment = None

            processed_reviews.append({
                'name': review.name,
                'relativePublishTimeDescription': review.relativePublishTimeDescription,
                'rating': review.rating,
                'text': review.text,
                'originalText': review.originalText,
                'authorAttribution': review.authorAttribution,
                'publishTime': review.publishTime,
                'sentiment': sentiment
            })

        average_sentiment = sum(review_sentiments) / len(review_sentiments) if review_sentiments else None

        res.append({
            'formattedAddress': place.formattedAddress,
            'location': place.location,
            'displayName': place.displayName,
            'reviews': processed_reviews,
            'photos': place.photos,
            'averageSentiment': average_sentiment
        })
    
    sorted_res = sorted(res, key=lambda x: x['averageSentiment'], reverse=True)
    limited_res = sorted_res[:limit]

    return limited_res