import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from transformers import TFBertModel, BertTokenizer
import numpy as np
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import re
import string

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


def print_pred(text):
    res = prep_pred(text)
    res = model.predict(res)
    res = np.argmax(res[0]) + 1
    return print(f"Review: {text}\nPred: {res} bintang")

text1 = "Tempatnya sangat bagus, sejuk, suasananya indah"
text2 = "Tempatnya sangat buruk, bangunan rusak, saya tidak rekomendasikan"
text3 = "Tempatnya biasa saja, tidak terlalu bagus, tidak terlalu buruk"
text4 = "Tempatnya sangat kotor, tidak terawat, tidak nyaman"
text5 = "Tempatnya sangat bersih, terawat, nyaman"

print_pred(text1)
print_pred(text2)
print_pred(text3)
print_pred(text4)
print_pred(text5)