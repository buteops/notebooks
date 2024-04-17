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

"""
   Keywords:
   - False     - await     - elif      - if        - or        - with
   - None      - in        - else      - import    - pass      - match
   - True      - break     - except    - in        - raise     - case
   - and       - class     - finally   - is        - return    - *args
   - as        - continue  - for       - lambda    - yield     - **kwargs
   - assert    - def       - from      - nonlocal  - try       - type
   - async     - del       - global    - not       - while
"""