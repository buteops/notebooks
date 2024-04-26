#!/usr/bin/env python3

from __future__ import annotations
import os, sys, glob, random
from pathlib import Path
sys.path.append('/home/adalgiso/personal/mlopsency/')
import numpy as np
from typing import List
from datetime import datetime

import keras
from PIL import Image, ImageDraw
from utilizers.utils_data import rps_download


SHAPES = (150, 150, 3)
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.4

def data_generator(dpath: Path, subset: str):
   return keras.utils.image_dataset_from_directory(
      directory = dpath,
      labels='inferred',
      label_mode='categorical',
      color_mode='rgb',
      batch_size=BATCH_SIZE,
      image_size=SHAPES[:2],
      seed=123,
      validation_split=VALIDATION_SPLIT,
      subset=subset,
   )
   
def get_random_image(dpath: Path, class_names: List):
  random_subdir = random.choice(class_names)
  images = glob.glob(os.path.join(dpath, random_subdir, '*.png'))
  selected_image_paths = random.choice(images)
  return selected_image_paths


class RPSCallback(keras.callbacks.Callback):
   def on_epoch_end(self, epoch, logs={}):
      if logs.get('accuracy') is not None and logs.get('accuracy') > 0.95:
         print("\nReached more 95% validation accuracy so cancelling training!")
         self.model.stop_training = True
         

class RockPaperScissors(keras.models.Model):
   def __init__(self, classes):
      super(RockPaperScissors, self).__init__()
      
      self._conv2d_1 = keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=SHAPES)
      self._maxpool2d_1 = keras.layers.MaxPooling2D((2, 2))
      self._conv2d_2 = keras.layers.Conv2D(64, (3,3), activation='relu')
      self._maxpool2d_2 = keras.layers.MaxPooling2D((2, 2))
      self._conv2d_3 = keras.layers.Conv2D(128, (3,3), activation='relu')
      self._maxpool2d_3 = keras.layers.MaxPooling2D((2, 2))
      self._flatten = keras.layers.Flatten()
      self._dense_1 = keras.layers.Dense(512, activation='relu')
      self._dropout = keras.layers.Dropout(0.5)  # Regularization: Dropout
      self._classifier = keras.layers.Dense(classes, activation='softmax')
      
   def call(self, input_shape):
      x = self._conv2d_1(input_shape)
      x = self._maxpool2d_1(x)
      x = self._conv2d_2(x)
      x = self._maxpool2d_2(x)
      x = self._conv2d_3(x)
      x = self._maxpool2d_3(x)
      x = self._flatten(x)
      x = self._dense_1(x)
      x = self._dropout(x)
      x= self._classifier(x)
      return x
      

if __name__ == '__main__':
   
   RESULTS = 'assets/results'
   RPS_DATA = 'datasets/rps/'
   if not os.path.isdir(RPS_DATA): rps_download()
   train_generator = data_generator(RPS_DATA, 'training')
   validation_generator = data_generator(RPS_DATA, 'validation')
   class_name = train_generator.class_names
   
   rps_model = RockPaperScissors(classes = len(class_name))
   rps_model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics=['accuracy'])
   rps_model.fit(train_generator, epochs = 10, validation_data = validation_generator, callbacks=[RPSCallback()])
   
   img = get_random_image(RPS_DATA, class_name)
   pred_img = keras.preprocessing.image.load_img(img, target_size=(150,150))
   x = keras.preprocessing.image.img_to_array(pred_img)
   x = np.expand_dims(x, axis=0)
   images = np.vstack([x])
   classes = rps_model.predict(images, batch_size=BATCH_SIZE)
   max_index = np.argmax(classes)
   class_label = class_name[max_index]
   print("Class label: " + class_label)
   
   
   # Generate Predicted + Labeled Image
   pil_img = Image.open(img)
   pred_labels = ImageDraw.Draw(pil_img)
   pred_labels.text((75,75), f"Class label: {class_label}", fill = (255, 0, 0))
   pil_img.show()
   pil_img.save("../assets/results/plain_rockpaperscissors.png")
