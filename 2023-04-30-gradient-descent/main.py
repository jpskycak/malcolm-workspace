"""
New problem:

Given the points (x, sin(x)) for x=0, 0.2, 0.4, .., 3

Find the best fit of the function

y = 2^(a1 x + b1) + 3^(a2 x + b2) + 4^(a3 x + b3) + 5^(a4 x + b4)

to those points
"""

import matplotlib.pyplot as plt
import numpy as np
from helpers import *

# GLOBALS

#expected_params = [0, 0, 0, 0, 0, 0, 0, -2, 2,
#0]  [0, -5, -5, 5, 5, 0, 0, 0, 0, 0]
params = [(np.random.rand() - 0.5) / 0.5 for _ in range(8)]
reg_scalar = 0

batch_size = 5


def expected_f(x):
  return x**3 - x


num_points = int(len(params) * batch_size)

endpoints = [-1, 1]

data = generate_yvals(expected_f, [
  endpoints[0] + (endpoints[1] - endpoints[0]) * n / num_points
  for n in range(num_points)
])

alpha = 0.05
iterations = 10001


def f(x):
  f = 0
  for i in range(0, len(params), 2):
    base = 1 + np.ceil((i + 1) / 2)
    linear = params[i] * x
    f += params[i+1] * base**linear
    #f += np.sin(linear)
  return f


"""
  for i in range(len(params)):
    if i % 2:
      f += params[i] * np.cos(np.ceil((i + 1) / 2) * x)
    else:
      f += params[i] * np.sin(np.ceil((i + 1) / 2) * x)
"""

# BEGIN GRADIENT DESCENT PROCEDURE

initial_mse = calc_mse(data, f)
initial_reg = calc_reg(params) * reg_scalar
print(
  f'Initial MSE = {initial_mse}, Initial REG = {initial_reg}, Initial COST = {initial_mse + initial_reg}'
)

data_indices = []
for i in range(len(data)):
  data_indices.append(i)

for n in range(iterations):

  # calc gradient
  grad = []
  for i in range(len(params)):
    grad.append(0)

  random_set_indices = np.random.choice(data_indices,
                                        int(len(data) / batch_size))

  for i in random_set_indices:
    [x, y] = data[i]

    # MSE = 1/N sum (f(x) - y)^2
    # REG = sum (param^2)
    # COST = MSE + REG
    # dMSE/dParam = 1/N sum 2(f(x) - y) df/dParam
    # dREG/dParam = 2 * Param

    num_points = len(data)
    diff = f(x) - y
    for i in range(len(grad)):
      # f(x) = p0 + p1 x + p2 x^2 + ...
      # grad_MSE = 2 * diff * (x**i) / num_points

      # f(x) = p0 cos(x) + p1 sin(x) + p2 cos(2x) + p3 sin(2x) +...
      base = 1 + np.ceil((i + 1) / 2)

      if i % 2 == 0:
        linear = params[i] * x
        grad_MSE = 2 * diff * x * params[i+1]*base**linear * np.log(base) / num_points
        #grad_MSE = 2 * diff * np.cos(linear) * x / num_points
      else:
        linear = params[i - 1] * x
        #grad_MSE = 2 * diff * np.cos(linear) / num_points
        grad_MSE = 2 * diff * base**linear / num_points

      grad_REG = 2 * params[i] * reg_scalar
      grad[i] += grad_MSE + grad_REG

  # update params
  for i in range(len(params)):
    params[i] -= alpha * grad[i]

  # log/plot
  if n % 500 == 0:
    mse = calc_mse(data, f)
    reg = calc_reg(params) * reg_scalar
    print(
      f'{n+1} iterations complete: MSE = {mse}, REG = {reg}, COST = {mse + reg}'
    )

plotcurve(f, endpoints)

print(params)
plotpoints(data)

plt.title('final plot')
plt.savefig('plot.png')
