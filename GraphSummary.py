import networkx as nx
import json


class GraphSummary():
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def __str__(self) -> str:
        return self.summary()

    def summary(self) -> str:
        """Return a summary of the graph."""
        G = self.graph
        summary_text = f"{self.graph.name}\n"
        summary_text += f"Number of nodes: {len(G.nodes)}\n"
        summary_text += f"Number of edges: {len(G.edges)}\n"
        summary_text += f"Average degree: {sum(dict(G.degree).values()) / len(G.nodes)}\n"
        summary_text += f"Density: {nx.density(G)}\n"
        return summary_text

    def info(self) -> str:
        """Return the graph as a JSON string."""
        graph_dict = nx.to_dict_of_lists(self.graph)  # 将Graph对象转换为字典
        graph_str = json.dumps(graph_dict)  # 将字典转换为字符串
        return graph_str


if __name__ == '__main__':
    import matplotlib
    import community as community_louvain
    import matplotlib.pyplot as plt
    matplotlib.use('Agg')

    datasets = {
        "karate_club_graph": nx.karate_club_graph(),
        "davis_southern_women_graph": nx.davis_southern_women_graph(),
        "florentine_families_graph": nx.florentine_families_graph(),
        "les_miserables_graph": nx.les_miserables_graph(),
    }

    for name in datasets:
        G = datasets[name]
        s = GraphSummary(G)
        print(s.summary())
        print(s.info())

        # compute the best partition
        partition = community_louvain.best_partition(G)
        print('Number of communities:', len(set(partition.values())))
        print('modularity:', community_louvain.modularity(
            partition, G))  # modularity

        # 获取每个社区的节点列表
        communities = {}
        for node, community in partition.items():
            if community not in communities:
                communities[community] = []
            communities[community].append(node)

        # 创建并保存每个社区的子图
        for community, nodes in communities.items():
            subgraph = G.subgraph(nodes)
            # nx.draw(subgraph)
            # plt.savefig(f'figs/community_{community}.png')

        # draw the graph
        pos = nx.spring_layout(G)

        # color the nodes according to their partition
        cmap = matplotlib.colormaps.get_cmap('viridis')

        nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                               cmap=cmap, node_color=list(partition.values()))
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        plt.savefig(f'figs/{name}.png')
