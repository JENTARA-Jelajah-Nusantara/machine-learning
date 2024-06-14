import pandas as pd
import json
import sys
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import re
import string

if len(sys.argv) != 2:
    print("Need 2 args")
    sys.exit("Usage: python clean_data.py path/to/data.csv")

factory = StopWordRemoverFactory()
stopword_remover = factory.create_stop_word_remover()
stopwords = set(factory.get_stop_words())


def clean(text):
    text = text.replace('\n', ' ')
    text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    words = [word for word in words if word not in stopwords]
    text = ' '.join(words)
    return text


df = pd.read_csv(str(sys.argv[1]))

reviews_ratings = []
reviews = df[['user_reviews']]

for i in reviews['user_reviews']:
    if isinstance(i, str):
        place_all_reviews = json.loads(i)
        for people_review in place_all_reviews:
            review_rating = {
                'Rating': people_review.get('Rating', None),
                'Review': people_review.get('Description', '')
            }
            reviews_ratings.append(review_rating)

reviews_ratings_df = pd.DataFrame(reviews_ratings)

reviews_ratings_df["Review"] = reviews_ratings_df["Review"].apply(clean)

reviews_ratings_df.to_csv('filtered_cleaned_data.csv', index=False)
