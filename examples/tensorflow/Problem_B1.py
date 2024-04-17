# Given two arrays, train a neural network model to match the X to the Y.
# Predict the model with new values of X [-2.0, 10.0]
# We provide the model prediction, do not change the code.
#
# The test infrastructure expects a trained model that accepts
# an input shape of [1]
# Do not use lambda layers in your model.
#
# Please be aware that this is a linear model.
# We will test your model with values in a range as defined in the array to make sure your model is linear.
#
# Desired loss (MSE) < 1e-3

import numpy as np
# import tensorflow as tf
# import keras
from pathlib import Path
import os

pdfClass = 'PDFMalicious'
fpath = Path(os.getcwd()).resolve().parent.parent / f'datasets/CICDatasets/{pdfClass}/{pdfClass}_1'

for entry in fpath.iterdir():
    print(entry)


# def solution_B1():
#     # y = 2x + 1
#     X = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], dtype=float)
#     Y = np.array([5.0, 7.0, 9.0, 11.0, 13.0, 15.0, 17.0], dtype=float)

#     model = keras.models.Sequential([
#         keras.layers.Dense(units=1, input_shape=[1])
#     ])

#     model.compile(loss=keras.losses.MeanSquaredError(), optimizer=keras.optimizers.SGD())
#     model.fit(X, Y, epochs=100)

#     print(model.predict(np.array([-2.0, 10.0])))
#     return model

# if __name__ == '__main__':
#     model = solution_B1()