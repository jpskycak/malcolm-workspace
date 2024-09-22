#current path maker code


def find_all_paths(network, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if path.count(start) == 2:
        return []
    paths = []
    for node in network:
      for connection in node:
        if connection not in path:
          branches = find_other_connections(network, start)
          for branch in branches:
            new_paths = find_all_paths(network, branch, end, path)
            for p in new_paths:
              if paths.count(p) == 0:
                paths.append(p)
    return paths

def find_other_connections(network, value):
  branches = []
  for node in network:
    node_connected = False
    for i in range(len(node)):
      if node[i] == value:
        node_connected = True
    for i in range(len(node)):
      if node_connected and node[i] != value and branches.count(node[i]) == 0:
        branches.append(node[i])
  return branches


network = [['TOP',1],['TOP',2],[1,3],[1,4],[2,3],[2,5],[3,4],[3,5],[4,'BOTTOM'],[5,'BOTTOM']]

print(find_all_paths(network, 'TOP', 'BOTTOM'))
