import sys
sys.path.append('/home/runner/malcolm-workspace/2023-08-13-matrix-class')

from matrix import *

import numpy as np
import matplotlib.pyplot as plt

ground_coefficients = [0.1, 0.2, 0.3, 0, 0.05, 0]

def get_ground_coefficients():
  return ground_coefficients

def eval_coefficients(coefficients, x):
  result = 0
  for i in range(len(coefficients)):
    c = coefficients[i]
    result += c * (x**i)
  return result

def plot_ground_coefficients(coefficients, start_x, stop_x):
  thick = True
  plot_coefficients(coefficients, start_x, stop_x, thick)

def plot_coefficients(coefficients, start_x, stop_x, thick=False):
  xs = np.linspace(start_x, stop_x, 20)
  ys = []
  for x in xs:
    y = eval_coefficients(coefficients, x)
    ys.append(y)
  if thick:
    plt.plot(xs, ys, linewidth=7.0)
  else:
    plt.plot(xs, ys)
    
def tweak(coefficients, num_copies):
  copies = [coefficients]

  for num in range(num_copies):
    copy = []

    for coefficient in coefficients:
      tweaked_coefficient = coefficient + np.random.rand() - 0.5
      copy.append(tweaked_coefficient)

    copies.append(copy)

  return copies


def get_cost(coefficients, start_x, end_x):
  cost = 0
  for x in np.linspace(start_x, end_x, 50):
    eval = eval_coefficients(coefficients, x)
    truth = eval_coefficients(ground_coefficients, x)
    diff = eval - truth
    cost += diff**2
  return cost

def choose_best_function(coefficients, start_x, end_x):
  copies = tweak(coefficients, 20)
  
  costs = []
  for copy in copies:
    cost = get_cost(copy, start_x, end_x)
    costs.append(cost)
  best_func_index = costs.index(np.min(costs))
  return copies[best_func_index]


def generate_weights(layer_sizes):
  # Note: Include bias nodes in layer sizes, including output layer
  weights = []
  for i in range(len(layer_sizes) - 1):
    weight = []
    for j in range(layer_sizes[i + 1] - 1):
      weight_row = []
      for k in range(layer_sizes[i]):
        weight_row.append(2 * np.random.rand() - 1)
      weight.append(weight_row)
    weight = Matrix(weight)
    weights.append(weight)
  return weights
