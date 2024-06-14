from transformers import TFBertModel, BertTokenizer
import tensorflow as tf
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

MODEL_PATH = '/home/alridho/Coding/jentara/sentimen.h5'
CHECKPOINT = "indobenchmark/indobert-base-p2"

model = tf.keras.models.load_model(MODEL_PATH)
tokenizer = BertTokenizer.from_pretrained(CHECKPOINT)
factory = StopWordRemoverFactory()
stopword_remover = factory.create_stop_word_remover()
stopwords = set(factory.get_stop_words())