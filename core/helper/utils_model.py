from pathlib import Path
import sys
sys.path.append(Path.cwd().as_posix())
import tensorflow as tf

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="models/mobilenet_quant.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("Input details:")
print(input_details)
print("\nOutput details:")
print(output_details)

# Get total number of layers
num_layers = interpreter.get_tensor_details()
print("\nNumber of layers:", len(num_layers))

# for layer in interpreter.get_tensor_details():
#   layer_name = layer['name']
  # layer_type = layer['dtype']
  # layer_shape = layer['shape']
  # layer_parameters = interpreter.get_tensor(layer['index'])

  # print(layer_name)
  # print("Type:", layer_type)
  # print("Shape:", layer_shape)
  # print("Parameters:")
  # print(layer_parameters)
