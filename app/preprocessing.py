import re
import string
import tensorflow as tf
from app.config import tokenizer, stopwords

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
