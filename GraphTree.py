import networkx as nx


class GraphNode():
    def __init__(self, graph: nx.Graph, parent=None):
        self.graph = graph
        self.parent = parent
        self.children = {}

    def add_child_node(self, graph: nx.Graph) -> 'GraphNode':
        child_node = GraphNode(graph, self)
        self.children[graph.name] = child_node
        return child_node

    def get_parent(self) -> 'GraphNode':
        return self.parent

    def get_dataset(self) -> nx.Graph:
        cur_node = self
        while cur_node.parent.graph is not None:
            cur_node = cur_node.parent
        return cur_node.graph
