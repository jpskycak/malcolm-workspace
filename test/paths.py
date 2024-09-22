"""
Given network
node: [children]
d = {
  0: [1,2],
  1: [2,3],
  2: [1,3],
  3: []
}

Want to convert this into list of paths

[
  [0,1,3],
  [0,1,2,3],
  [0,2,3],
  [0,2,1,3]
]
"""

def find_source_node(d):
  all_children = []
  
  for node in d:
    for child in d[node]:
      all_children.append(child)

  for node in d:
    if node not in all_children:
      source = node

  return source

def find_paths_old(d, source_node, path=[], paths=[]):
  # for each source node, follow paths all the way forward to leaf nodes
  # if we're ever on a path that doubles back, kill it
  path.append(source_node)
  for child in d[source_node]:
    if child not in path:
      find_paths_old(d, child, path, paths)

  if d[source_node] == []:
    paths.append(path)
    path = []
  print(paths)

def find_paths_old2(d, source_node, paths=[]):
  # for each source node, follow paths all the way forward to leaf nodes
  # if we're ever on a path that doubles back, kill it

  # kick things off (if things haven't yet been kicked off)
  if paths == []:
    paths = [[source_node]]

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
    find_paths_old2(d, 0, extended_paths)
  else:
    print(paths)
    return paths

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
  
d = {
  0: [1,2],
  1: [2,3],
  2: [1,3],
  3: []
}

actual_values = {1: [0,1], 
                 2: [1,3], 
                 3: [1,2], 
                 2: [0,2], 
                 5: [2,3]
              }


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
  for i in range(len(unique_pairs)):
    effective_resistance = pair_counts[i] * get_key_from_value(values, unique_pairs[i])
    effective_resistances[effective_resistance] = unique_pairs[i]

  grid = []
  for list in pairs:
    row = []
    for pair in list:
      if pair[0] > pair[1]:
        pair = [pair[1], pair[0]]
      row.append(get_key_from_value(effective_resistances, pair))
    grid.append(row)

  return grid


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

#print(calc_coords(make_pairs(find_paths(d))))
#print(calc_grid(make_pairs(find_paths(d)), actual_values))


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


print(nodes_from_locations([[0,1],[0,2],[1,2]]))