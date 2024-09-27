import sys
sys.path.append('/workspace/malcolm-workspace/2023-08-13-matrix-class/matrix.py')

from matrix import *
from helpers import *
import numpy as np
import matplotlib.pyplot as plt

class NeuralNet:

  def __init__(self, weights):
    self.weights = weights
    self.num_layers = len(self.weights) + 1

  def show(self):
    for matrix in self.weights:
      matrix.show()
      print(' ')

  def compute_next_layer(self, layer_index, previous_activations):
    layer_weights = self.weights[layer_index]
    if layer_weights.num_cols != len(previous_activations):
      previous_activations.append(1)
    nested_pa = []
    for activation in previous_activations:
      nested_pa.append([activation])
    pa_matrix = Matrix(nested_pa)
    #print(f'layer_weights')
    #layer_weights.show()
    #print(f'pa_matrix')
    #pa_matrix.show()
    next_activations = layer_weights.mult(pa_matrix)

    if next_activations.num_cols != 1:
      raise Exception('Activation matrix non-linear')

    next_activations = next_activations.column(0)
    for i in range(len(next_activations)):
      next_activations[i] = np.tanh(next_activations[i])
    return next_activations

  def compute_all_layers(self, input_layer):
    activations = self.compute_next_layer(0, input_layer)
    A = [input_layer]
    for i in range(self.num_layers - 2):
      #if i == self.num_layers - 3:
      #  activations.pop(-1)
      #attempted fix for extra 1 in output layer, created more problems
      A.append(activations)
      activations = self.compute_next_layer(i + 1, activations)
    A.append(activations)
    for i in range(len(activations)):
      activations[i] = np.arctanh(activations[i])
    return activations, A

  def make_child(self, variance):
    child = []
    for W in self.weights:
      new_matrix = W.make_random_copy(variance)
      child.append(new_matrix)
    child = NeuralNet(child)
    
    return child


  def find_cost(self, input_layers, ideal_output_layers):
    cost = 0
    for i in range(len(input_layers)):
      output_layer, activations = self.compute_all_layers(input_layers[i])
      for j in range(len(output_layer)):
        cost += (output_layer[j] - ideal_output_layers[i][j])**2
    
    return cost

  
  def compute_final_RSS(self, input_layers, ideal_output_layers):
    RSS = 0
    for i in range(len(input_layers)):
      output_layer = self.compute_all_layers(input_layers[i])[0]
      for j in range(len(output_layer)):
        RSS += (output_layer[j] - ideal_output_layers[i][j]) ** 2

    return RSS / len(input_layers)

  #backpropogation stuff
  def get_RSSs(self, layer_index, previous_RSSs, activations):
    layer_weights = self.weights[layer_index]
    layer_activations = activations[layer_index + 1]
    if layer_activations[-1] == 1:
      layer_activations.pop(-1)
      previous_RSSs.pop(-1)
    if len(layer_activations) != len(previous_RSSs):
      raise Exception('Activations do not match RSSs')
    formatted_vector = []
    for i in range(len(layer_activations)):
      formatted_vector.append((1 - layer_activations[i]**2) * previous_RSSs[i])
    formatted_vector = [formatted_vector]
    vector = Matrix(formatted_vector)
    new_RSSs = vector.mult(layer_weights)
    return new_RSSs
    


class Generation:
  def __init__(self, parent_nets):
    self.nets = parent_nets

  def show(self):
    for net in self.nets:
      net.show()
      print('\n \n')


  def make_children(self, num_children):
    children = self.nets

    for net_index in range(len(self.nets)):
      for num in range(num_children):
        child = self.nets[net_index].make_child(0.1)
        children.append(child)

    return children

  def find_best_children(self, input_layers, ideal_output_layers, num_children, num_survive):
    children = self.make_children(num_children)
    best_children = []
    costs = []
    for child in children:
      cost = child.compute_final_RSS(input_layers, ideal_output_layers)
      costs.append(cost)

    for i in range(num_survive):
      best_child_index = costs.index(np.min(costs))
      best_children.append(children[best_child_index])
      children.pop(best_child_index)
      costs.pop(best_child_index)

    return best_children

  def iterate(self, input_layers, ideal_output_layers, num_children_per_net=20, num_parent_nets=1):
    next_gen = self.find_best_children(input_layers, ideal_output_layers, num_children_per_net, num_parent_nets)
    next_gen = Generation(next_gen)
    return next_gen

  def compute_RSS(self, input_layers, ideal_output_layers):
    RSS = 0
    for net in self.nets:
      RSS += 100 * net.compute_final_RSS(input_layers, ideal_output_layers) # to get RSSs on a reasonable scale
    return RSS / len(self.nets)

net_size = [2, 5, 5, 5, 5, 5, 2]
points = 100
domain = [-1, 1]
iterations = 1000
child_nets = 50
parent_nets = 5
coefficients = [1, 2.8, 0.5, -1, -5.2, 1]

weights = generate_weights(net_size)
parent_net = NeuralNet(weights)
inputs = np.linspace(domain[0], domain[1], points)
for i in range(len(inputs)):
  inputs[i] += random.random() * (domain[1] - domain[0])/ (2 * points) - (domain[1] - domain[0])/ (4 * points)
ideal_output_layers = []
input_layers = []
for input in inputs:
  ideal_output_layers.append([eval_coefficients(coefficients, input, 1)])
  input_layers.append([input])
generation = Generation([parent_net])
for i in range(iterations):
  generation = generation.iterate(input_layers, ideal_output_layers, child_nets, parent_nets)
  print(generation.compute_RSS(input_layers, ideal_output_layers))

  current_net = generation.nets[0]
  ideal_outputs = []
  outputs = []

  for i in range(len(input_layers)):
    outputs.append(current_net.compute_all_layers(input_layers[i])[0][0])
    ideal_outputs.append(ideal_output_layers[i][0])

  plt.plot(inputs, outputs)
  plt.plot(inputs, ideal_outputs)
  plt.savefig('2024-08-11-genetic-algorithm/neural_fitting.png')
  plt.clf()

final_net = generation.nets[0]
ideal_outputs = []
outputs = []

for i in range(len(input_layers)):
  print(final_net.compute_all_layers(input_layers[i])[0])
  outputs.append(final_net.compute_all_layers(input_layers[i])[0][0])
  print(ideal_output_layers[i])
  ideal_outputs.append(ideal_output_layers[i][0])
  print(' ')

plt.plot(inputs, outputs)
plt.plot(inputs, ideal_outputs)
plt.savefig('2024-08-11-genetic-algorithm/neural_fitting.png')