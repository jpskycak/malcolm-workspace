import numpy as np
import matplotlib.pyplot as plt
from helpers import *
from neuralnet import *

ground_coefficients = get_ground_coefficients()
coefficients = [0, 0, 0, 0, 0, 0]
weights = generate_weights(3, 5, 5, 4)
start_x = -1
end_x = 1

plot_ground_coefficients(ground_coefficients, start_x, end_x)

for generation_num in range(100):
  print(f'Generation {generation_num}')
  print(f'   Coefficients = {coefficients}')
  print(f'   Cost = {get_cost(coefficients, start_x, end_x)}')
  print('')
  plot_coefficients(coefficients, start_x, end_x)  
  coefficients = choose_best_function(coefficients, start_x, end_x)

plot_ground_coefficients(coefficients, start_x, end_x)


plt.savefig('basic_fitting.png')