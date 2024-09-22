def calc_resistance(series_or_parallel, resistances):
  if series_or_parallel == "series":
    return calc_resistance_series(resistances)
  elif series_or_parallel == "parallel": 
     return calc_resistance_parallel(resistances)
  else:
    raise Exception(f'Invalid series_or_parallel: {series_or_parallel}')

def calc_resistance_series(resistances):
  r_eq = 0
  for i in range(len(resistances)):
    r_eq += resistances[i]
  return r_eq

def calc_resistance_parallel(resistances):
  r_eq_reciprocal = 0
  for i in range(len(resistances)):
    r_eq_reciprocal += 1/resistances[i]
  r_eq = 1/r_eq_reciprocal
  return r_eq

def solve_with_ratios(ratios, original_resistance):
  """
  2nd Approx:
  ratios = [1, 4/5]
  original_resistance = R

  R = 1 / (1/(Rleft) + 1/(Rleft * 4/5))

  original_resistance = 1 / (1/(Rleft * ratios[0]) + 1/(Rleft * ratios[1])) + ...

  1/original_resistance = 1/Rleft * (1/ratios[0] + 1/ratios[1]+...)
  R_left = original_resistance * (1/ratios[0] + 1/ratios[1]+...)
  R_next = R_left * ratios[1]
  """
  resistances = []
  
  R_left = original_resistance * calc_sum_reciprocals(ratios)
  for i in range(len(ratios)):
    resistances.append(R_left * ratios[i])
  return resistances

def calc_sum_reciprocals(array):
  sum = 0
  for i in range(len(array)):
    sum += 1/array[i]
  return sum

def calc_ratios(currents, indicies):
  ratios = []
  for i in range(len(indicies)):
    ratios.append(currents[indicies[0]]/currents[indicies[i]])
  
  return ratios

def calc_currents(resistances):
  """
  I_n = (R_total/R_n) * I_total      for parallel circuits
  because these are going to be usead in ratios, the I_total will cancel, and can be treated as 1.
  """
  branch_resistances = []
  currents = []
  
  for i in range(len(resistances)):
    R_branch = calc_resistance('series', resistances[i])
    branch_resistances.append(R_branch)

  R_total = calc_resistance('parallel', branch_resistances)

  for i in range(len(branch_resistances)):
    currents.append(R_total/branch_resistances[i])
    
  return currents

def find_paths(d):
  # for each source node, follow paths all the way forward to leaf nodes
  # if we're ever on a path that doubles back, kill it

  all_children = []

  for node in d:
    for child in d[node]:
      all_children.append(child)

  for node in d:
    if node not in all_children:
      source = node

  paths = [[source]]

  while True:

    # extend all paths
    keep_going = False

    extended_paths = []

    for path in paths:
      path_end = path[-1]
      for child in d[path_end]:
        if child not in path:
          keep_going = True
          extended_path = path + [child]

          extended_paths.append(extended_path)

      if d[path_end] == []:
        extended_paths.append(path)

    if keep_going:
      paths = extended_paths
    else:  
      return paths

def make_pairs(lists):
  list_pairs = []
  for list in lists:
    pairs = []
    for i in range(len(list)):
      if i != len(list) - 1:
        pair = [list[i],list[i+1]]
        pairs.append(pair)
    list_pairs.append(pairs)
  
  return list_pairs  

def get_key_from_value(d, value):
  for key, val in d.items():
    if val == value:
      return key

def calc_coords(pairs):
    unique_pairs = []
    pairs_and_indicies = {}
    rows = []
    columns = []
    final_list = []
    for list in pairs:
      for pair in list:
        if pair[0] > pair[1]:
          pair = [pair[1], pair[0]]
        if pair not in unique_pairs:
          unique_pairs.append(pair)
  
      for i in range(len(unique_pairs)):
        pairs_and_indicies[i] = unique_pairs[i]
  
    for list in pairs:
      index_list = []
      for pair in list:
        if pair[0] > pair[1]:
          pair = [pair[1], pair[0]]
        index_list.append(get_key_from_value(pairs_and_indicies, pair))
      final_list.append(index_list)
  
    for i in range(len(unique_pairs)):
      row_coords = []
      col_coords = []
      for j in range(len(final_list)):
        if i in final_list[j]:
          row_coords.append(j)
          for k in range(len(final_list[j])):
            if final_list[j][k] == i:
              col_coords.append(k)
      rows.append(row_coords) 
      columns.append(col_coords) 
    return rows, columns

def calc_grid(pairs, values):
  unique_pairs = []
  for list in pairs:
    for pair in list:
      if pair[0] > pair[1]:
        pair = [pair[1], pair[0]]
      if pair not in unique_pairs:
        unique_pairs.append(pair)
  
  pair_counts = []
  for pair in unique_pairs:
    pair_count = 0
    for list in pairs:
      for p in list:
        if p[0] > p[1]:
          p = [p[1], p[0]]
        if p == pair:
          pair_count += 1
    pair_counts.append(pair_count)
  
  effective_resistances = {}
  actual_resistances = []
  for i in range(len(unique_pairs)):
    effective_resistance = pair_counts[i] * get_key_from_value(values, unique_pairs[i])
    actual_resistance = get_key_from_value(values, unique_pairs[i])
    effective_resistances[effective_resistance] = unique_pairs[i]
    actual_resistances.append(actual_resistance)
  grid = []
  for list in pairs:
    row = []
    for pair in list:
      if pair[0] > pair[1]:
        pair = [pair[1], pair[0]]
      row.append(get_key_from_value(effective_resistances, pair))
    grid.append(row)
  
  return grid, actual_resistances

def nodes_from_locations(locations):
  nodes = [0]
  for trip in locations:
    if trip[0] not in nodes:
      nodes.append(trip[0])
    if trip[1] not in nodes:
      nodes.append(trip[1])
  nodes.sort()
  node_connections = {}
  for node in nodes:
    children = []
    for trip in locations:
      if trip[0] == node:
        children.append(trip[1])
    node_connections[node] = children
  
  return node_connections

def clean_data(resistors, locations):
  fix_order(resistors, locations)
  fix_duplicates(resistors, locations)

def fix_order(resistors, locations):
  for i in range(len(locations)):
    if locations[i][1] < locations[i][0]:
      locations[i] = [locations[i][1],locations[i][0]]
  
def fix_duplicates(resistors, locations):
  for i in range(len(locations)):
    if i > len(locations) - 1:
      break

    i = len(locations) - 1 - i
    while locations.count(locations[i]) > 1:
      last_instance = 0
      duplicate_indicies = [j for j, e in enumerate(locations) if e == locations[i]]
      duplicate_indicies = duplicate_indicies[::-1]
      for k in duplicate_indicies:
        if k == duplicate_indicies[0]:
          last_instance = resistors[k]
          resistors.pop(k)
          locations.pop(k)
        if k == duplicate_indicies[1]:
          resistors[k] = calc_resistance('parallel', [resistors[k],last_instance])
          i = k
          break
         
  return resistors, locations