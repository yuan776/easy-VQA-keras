from keras.preprocessing.text import Tokenizer
from keras.preprocessing.image import load_img, img_to_array
from keras.preprocessing.sequence import pad_sequences
import json
import os
from constants import *


print('\n--- Reading questions...')
def read_questions(path):
  with open(path, 'r') as file:
    qs = json.load(file)
  texts = [q[0] for q in qs]
  answers = [q[1] for q in qs]
  image_ids = [q[2] for q in qs]
  return (texts, answers, image_ids)
train_qs, train_answers, train_image_ids = read_questions('data/train/questions.json')
test_qs, test_answers, test_image_ids = read_questions('data/test/questions.json')
all_qs = train_qs + test_qs
print(f'Read {len(train_qs)} training questions and {len(test_qs)} testing questions.')


print('\n--- Reading answers...')
with open('data/answers.txt', 'r') as file:
  all_answers = [a.strip() for a in file]
num_answers = len(all_answers)
print(f'Found {num_answers} total answers.')


print('\n--- Reading training images...')
def read_images(dir):
  ims = []
  for filename in os.listdir(dir):
    if filename.endswith('.png'):
      ims.append(img_to_array(load_img(os.path.join(dir, filename))))
  return ims
train_ims = read_images('data/train/images')
test_ims = read_images('data/test/images')
im_shape = train_ims[0].shape
print(f'Read {len(train_ims)} training images and {len(test_ims)} testing images.')
print(f'Each image has shape {im_shape}.')


print('\n--- Fitting question tokenizer...')
texts = list(map(lambda q: q[0], all_qs))
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
vocab_size = len(tokenizer.word_index)
print(f'Found {vocab_size} words total.')


print('\n--- Converting questions to token sequences...')
def text_to_seq(texts):
  seqs = tokenizer.texts_to_sequences(texts)
  seqs = pad_sequences(seqs, maxlen=MAX_QUESTION_LEN)
train_seqs = text_to_seq(train_qs)
test_seqs = text_to_seq(test_qs)
