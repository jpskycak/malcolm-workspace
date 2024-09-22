from helpers import *

def run_test(test_function, test_input, desired_output):
  original_test_input = str(test_input)
  actual_output = test_function(*test_input)
  
  #if actual_output != desired_output:
  print()
  print(f'{test_function.__name__}')
  print('\tinput:', original_test_input)
  print('\toutput:', actual_output)
  print('\tdesired:', desired_output)

run_test(
  fix_duplicates,
  [
      [15, 15, 15, 15, 15, 15, 15, 15],
      [[0, 1], [1, 2], [0, 1], [0, 1], [1, 2], [0, 1], [0, 1], [1, 2]]
  ],
  ([3, 5], [[0, 1], [1, 2]])
)

run_test(
  fix_duplicates,
  [
      [6, 6, 6, 6, 6, 6, 6, 6],
      [[1, 2], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [1, 2]]
  ],
  ([1, 3], [[0, 1], [1, 2]])
)

run_test(
  fix_duplicates,
  [
      [2, 3, 4],
      [[2, 1], [1, 2], [0, 1]]
  ],
  ([2.5, 4], [[1, 2], [0, 1]])
)

#test nodes from locations next