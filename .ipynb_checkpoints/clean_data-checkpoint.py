import pandas as pd
import json
import sys

if len(sys.argv) != 2:
    print("Need 2 args")
    sys.exit("Usage: python clean_data.py path/to/data.csv")

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
reviews_ratings_df.to_csv('cleaned_data.csv', index=False)
