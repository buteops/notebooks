import jax.numpy as jnp
from jax import grad

# Define a simple function
def f(x):
    return x**2 + 3*x + 1

# Compute the gradient of the function
grad_f = grad(f)

# Evaluate the function and its gradient at a point
x_val = 2.0
result = f(x_val)
gradient_result = grad_f(x_val)

print("Function value at x =", x_val, ":", result)
print("Gradient value at x =", x_val, ":", gradient_result)
