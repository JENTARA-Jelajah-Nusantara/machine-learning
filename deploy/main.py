from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
from transformers import TFBertModel, BertTokenizer
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from typing import List
import numpy as np
import re
import string

class Review(BaseModel):
    text: str

class PlaceDetail(BaseModel):
    name: str
    image: str
    location: str
    description: str
    user_review: List[Review]

class Place(BaseModel):
    places: List[PlaceDetail]

model = tf.keras.models.load_model('/home/alridho/Coding/jentara/sentimen.h5')
factory = StopWordRemoverFactory()
stopword_remover = factory.create_stop_word_remover()
stopwords = set(factory.get_stop_words())
checkpoint = "indobenchmark/indobert-base-p2"
tokenizer = BertTokenizer.from_pretrained(checkpoint)

def prep_pred(text):
    text = text.replace('\n', ' ')
    text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    words = [word for word in words if word not in stopwords]
    text = ' '.join(words)
    tokenized_text = tokenizer.encode_plus(
        text,
        max_length=512,
        truncation=True,
        padding='max_length',
        add_special_tokens=True,
        return_tensors='tf',
    )
    return {
        'input_ids': tf.cast(tokenized_text['input_ids'], tf.float64),
        'attention_mask': tf.cast(tokenized_text['attention_mask'], tf.float64)
    }

app = FastAPI()

@app.post("/predict")
def predict(data: Place):
    res = []
    for place in data.places:
        res.append({
            'name': place.name,
            'image': place.image,
            'location': place.location,
            'description': place.description,
            'user_review': [
                {
                    'text': review.text,
                    'sentiment': int(np.argmax(model.predict(prep_pred(review.text))[0])) + 1
                }
                for review in place.user_review
            ],
            'average_sentiment': np.mean([
                int(np.argmax(model.predict(prep_pred(review.text))[0])) + 1
                for review in place.user_review
            ])
        })
    return res