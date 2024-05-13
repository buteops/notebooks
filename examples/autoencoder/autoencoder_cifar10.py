# try:
#    __import__('tensorflow')
#    __import__('tensorflow_datasets')
#    __import__('keras')
# except Exception as e:
#    import pip
#    print("The required modules are not installed!!")
#    pip.main(['install', 'tensorflow-cpu==2.16.1 keras==3.1.1 tensorflow-datasets==4.9.4'])
#    print("The required modules already installed!!")

from typing import List
import keras
import tensorflow as tf
import tensorflow_datasets as tfds
from keras.models import Sequential

