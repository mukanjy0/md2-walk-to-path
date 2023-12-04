def walk_to_path(walk):
  walk = walk.replace("(", "")
  walk = walk.replace(")", "")
  nodes = walk.split(",")

  map = dict()
  i = 0
  while i + 1 < len(nodes):
    node = nodes[i]
    if node in map.keys():
      j = map[node]
      for key in nodes[j+1:i]:
        map.pop(key)

      nodes = nodes[0:j] + nodes[i:]
      i = j
    else: 
      map[node] = i

    i += 1

  result = "("
  for node in nodes[0:-1]:
    result += node + ","
  result += nodes[-1] + ")"

  return result

walk = "(A,E,D,E,F,G,H,E,G,A)"
print(walk_to_path(walk))