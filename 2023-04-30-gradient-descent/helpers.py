import matplotlib.pyplot as plt
import numpy as np


def generate_yvals(f, xvals):
  randomized_coords = []

  for x in xvals:
    x = x + 0.05 * (np.random.rand() - 0.5) / 0.5
    #y = f(x) + 0.5 * (np.random.rand() - 0.5) / 0.5
    y = f(x) + 0.05 * (np.random.rand() - 0.5) / 0.5

    randomized_coords.append([x, y])
  return randomized_coords


def plotcurve(f, spread):
  step = (spread[1] - spread[0]) / 100
  range_start = int(spread[0] / step)
  range_stop = int(spread[1] / step)

  xvals = []
  yvals = []
  for x_div_step in range(range_start, range_stop):
    x = x_div_step * step
    xvals.append(x)
    yvals.append(f(x))

  plt.plot(xvals, yvals)


def calc_reg(params):
  regularization_term = 0
  for i in range(len(params)):
    regularization_term += params[i]**2
  return regularization_term


def plotpoints(data):
  xvals = []
  yvals = []
  for [x, y] in data:
    xvals.append(x)
    yvals.append(y)
  plt.scatter(xvals, yvals)


def calc_mse(data, f):
  MSE = 0
  for [x, y] in data:
    diff = f(x) - y #abs(f(x) - y) + 1
    MSE += diff**2
  MSE /= len(data)
  return MSE
