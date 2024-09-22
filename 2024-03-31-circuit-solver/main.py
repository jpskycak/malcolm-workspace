from helpers import *

resistors = [1,2,3,4,5]
locations = [[0,1], [0,2], [2,1], [1,3], [3,2]]

values = {}


def print_status(message):
  print()
  print(message)
  if values == {}:
    print('\tresistors:', resistors)
    print('\tlocations:', locations)
  else:
    print('\tvalues:', values)


clean_data(resistors, locations)

print_status('After cleaning data')

#checking both directions of resistors not attached to either end

highest_node = 0
for i in range(len(locations)):
  if locations[i][1] > highest_node:
    highest_node = locations[i][1]

for i in range(len(locations)):
  if locations[i][0] != 0 and locations[i][1] != highest_node:
    resistors.append(resistors[i])
    locations.append([locations[i][1], locations[i][0]])

print_status('After switching resistors')

#allowing the same value of resistor to occur more than once
#should not cause problems by slight change in resistances as they will be adjusted in far greater amounts below

differentiator = 0
for i in range(len(resistors)):
  if resistors.count(resistors[i]) > 1:
    resistors[i] += differentiator * 10**-15
    differentiator += 1

print_status('After differentiating same-value resistors')

#making dicionary

if len(locations) != len(resistors):
  raise Exception('locations does not match resistors')

for i in range(len(resistors)):
  values[resistors[i]] = locations[i]

print_status('After creating values dict')

#calculating current paths and coords of resistors in paths

nodes = nodes_from_locations(values.values())
paths = find_paths(nodes)
pairs = make_pairs(paths)
rows, columns = calc_coords(pairs)
resistances, actual_resistances = calc_grid(pairs, values)

def print_extra_vars(message):
  print()
  print(message)
  print('\trows:', rows)
  print('\tcolumns:', columns)
  print('\tresistances:', resistances)
  print('\tactual_resistances:', actual_resistances)

print_extra_vars('After creating extra variables')


#iterating adjusting resistances based on current ratios
iterations = 0
while True:
  iterations += 1
  if iterations > 5000:
    break
  currents = calc_currents(resistances)
  if 0 in currents:
    break

  for j in range(len(rows)):

    ratios = calc_ratios(currents, rows[j])
    new_resistances = solve_with_ratios(ratios, actual_resistances[j])

    for k in range(len(columns[j])):
      resistances[rows[j][k]][columns[j][k]] = new_resistances[k]

  if iterations % 500 == 0:
    print_extra_vars(f'After iteration {iterations}')

branch_resistances = []

for i in range(len(resistances)):
  R_branch = calc_resistance('series', resistances[i])
  branch_resistances.append(R_branch)

R_total = calc_resistance('parallel', branch_resistances)



# just some printing stuff
# dw abt it

print()
print('Final printout')
print('\tresistance:', R_total)
print('\tpairs:', pairs)

resistor_currents = {}
unique_pairs = []
for i in range(len(pairs)):
  for j in range(len(pairs[i])):
    negative = False
    if pairs[i][j][1] < pairs[i][j][0]:
      pairs[i][j] = [pairs[i][j][1], pairs[i][j][0]]
      negative = True
    if pairs[i][j] not in unique_pairs:
      unique_pairs.append(pairs[i][j])

print('\tunique_pairs:', unique_pairs)

for pair in unique_pairs:
  resistor_current = 0
  for i in range(len(pairs)):
    if pair in pairs[i]:
      if not negative:
        resistor_current += currents[i]
      else:
        resistor_current -= currents[i]
  resistor_currents[str(pair)] = resistor_current

print()
for key, val in resistor_currents.items():
  print(f'{key}: {val}')
