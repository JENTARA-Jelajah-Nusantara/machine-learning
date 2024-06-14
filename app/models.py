from pydantic import BaseModel
from typing import List, Optional


class Location(BaseModel):
    latitude: float
    longitude: float


class Text(BaseModel):
    text: Optional[str] = None
    languageCode: Optional[str] = None


class AuthorAttribution(BaseModel):
    displayName: Optional[str] = None
    uri: Optional[str] = None
    photoUri: Optional[str] = None


class Review(BaseModel):
    name: Optional[str] = None
    relativePublishTimeDescription: Optional[str] = None
    rating: Optional[int] = None
    text: Optional[Text] = None
    originalText: Optional[Text] = None
    authorAttribution: Optional[AuthorAttribution] = None
    publishTime: Optional[str] = None


class Photo(BaseModel):
    name: Optional[str] = None
    widthPx: Optional[int] = None
    heightPx: Optional[int] = None
    authorAttributions: Optional[List[AuthorAttribution]] = []


class DisplayName(BaseModel):
    text: Optional[str] = None
    languageCode: Optional[str] = None


class Place(BaseModel):
    formattedAddress: Optional[str] = None
    location: Optional[Location] = None
    displayName: Optional[DisplayName] = None
    reviews: Optional[List[Review]] = []
    photos: Optional[List[Photo]] = []


class PlacesData(BaseModel):
    places: Optional[List[Place]] = []