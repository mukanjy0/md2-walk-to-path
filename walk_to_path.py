import networkx as nx
import matplotlib.pyplot as plt


def visualize_graph(V: list, E=list, directed=False, walk=None, colored_edges=None, colors=['red', 'blue', 'black'], title=None):
    def get_undirected_graph(V: list, E=list):
        G = nx.Graph()
        G.add_nodes_from(V)
        G.add_edges_from(E)

        return G

    def get_directed_graph(V: list, E=list):
        edges = list()
        for [u, v] in E:
            edges.append((u, v))
            if u != v:
                edges.append((v, u))
        E = edges

        G = nx.DiGraph()
        G.add_nodes_from(V)
        G.add_edges_from(E)

        return G

    G = get_directed_graph(V, E) if directed else get_undirected_graph(V, E)
    pos = nx.spring_layout(G)

    if colored_edges is not None and walk is not None:
        if colors is None:
            colors = ['red', 'blue', 'black']
        edge_colors = [colors[0] if [u, v] in colored_edges or [v, u] in colored_edges
                       else colors[1] if [u, v] in walk or [v, u] in walk
                       else colors[2] for [u, v] in G.edges()]
    elif colored_edges is not None:
        if colors is None:
            colors = ['red', 'black']
        edge_colors = [colors[0] if [u, v] in colored_edges or [v, u] in colored_edges
                       else colors[1] for [u, v] in G.edges()]
    elif walk is not None:
        if colors is None:
            colors = ['green', 'black']
        edge_colors = [colors[0] if [u, v] in walk or [v, u] in walk
                       else colors[1] for [u, v] in G.edges()]
    else:
        edge_colors = ['black' for edge in G.edges()]


    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue",
            font_weight="bold", font_color='black', edge_color=edge_colors)
    if title is None:
        title = "Graph"
    plt.title(title)
    plt.show()


def walk_to_path(V, E, walk: str):
    """
  Receives a walk in compressed format (tuple of vertices).
    Example: (A,B,C,B) for G(V,E) : V = {A, B, C}, E = {{A, B}, {B, C}, {A, C}}

  Returns a path in compressed format, derived from the walk received as an argument.
    Example: (A,B,C,B) -> (A,B)
  """
    walk = walk.replace("(", "")
    walk = walk.replace(")", "")
    nodes = walk.split(",")

    walk_edges = []
    for i in range(1, len(nodes)):
        walk_edges.append([nodes[i-1], nodes[i]])

    map = dict()
    i = 0
    visualize_graph(V, E)
    while i < len(nodes):
        node = nodes[i]
        if node in map.keys():
            j = map[node]

            prev = node
            colored_edges = list()

            for key in nodes[j + 1:i]:
                map.pop(key)
                colored_edges.append([prev, key])
                prev = key
            colored_edges.append([prev, node])
            visualize_graph(V, E, walk=walk_edges, colored_edges=colored_edges, colors=['red', 'blue', 'black'], title="Graph with redundant sub-walk")

            nodes = nodes[0:j] + nodes[i:]
            walk_edges = []
            for i in range(1, len(nodes)):
                walk_edges.append([nodes[i-1], nodes[i]])

            i = j
        else:
            map[node] = i

        i += 1

    result = "("
    path_edges = list()
    for i in range(len(nodes) - 1):
        result += nodes[i] + ","
        path_edges.append([nodes[i], nodes[i+1]])
    result += nodes[-1] + ")"

    visualize_graph(V, E, walk=path_edges, colors=['green', 'black'], title="Path")

    return result


