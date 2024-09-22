# slope calculator
# advance x,y, and t
# store points for plotting
# repeat
# plot

import matplotlib.pyplot as plt
import random as rand

x = 10
y = 100
w = 100
numsteps = 100000
stepsize = 0.01
xpoints = []
ypoints = []
wpoints = []
tpoints = []

# a and d: base reproductive rate
# b and e: num deer wolf eats per time t
# c and g: death rate
# f: deer population cap

def dw_dt(y, w, g, h, i):
  wild_card = 5 * (rand.random() - 0.5)
  if w > i:
    g += 0.01
  return - y*w * g + w * h + wild_card

def dx_dt(x, y, a, b, f):
  wild_card = 5 * (rand.random() - 0.5)
  if x > f:
    b += 0.1
  return x*y * a - x * b + wild_card
  
def dy_dt(x, y, w, c, d, e, j):
  wild_card = 5 * (rand.random() - 0.5)
  if y > e:
    c += 0.01
  return - x*y * c + y*w * d + wild_card

def equation_evaluator(x, y, w, dx_dt, dy_dt, dw_dt):
  change_in_x = dx_dt(x, y, 0.08, 0.9, 25)
  change_in_y = dy_dt(x, y, w, 0.04, 0.003, 80, 0.1)
  change_in_w = dw_dt(y, w, 0.03, 0.4, 80)
  return [change_in_x, change_in_y, change_in_w]

def euler_estimator(x, y, w, dx_dt, dy_dt, dw_dt):
  for i in range(numsteps):
    change = equation_evaluator(x, y, w, dx_dt, dy_dt, dw_dt)
    x += change[0] * stepsize
    y += change[1] * stepsize
    w += change[2] * stepsize
    if x < 0:
      x = 10
    if y < 0:
      y = 0
    if w < 0:
      w = 0
    if w > 120:
      w = 100
    xpoints.append(x)
    ypoints.append(y)
    wpoints.append(w)
    #print([x,y])
    tpoints.append(i * stepsize)
  plt.plot(tpoints, xpoints)
  plt.plot(tpoints, ypoints)
  plt.plot(tpoints, wpoints)
  plt.savefig('plot.png')

euler_estimator(x, y, w, dx_dt, dy_dt, dw_dt)