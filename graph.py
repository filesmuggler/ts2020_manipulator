import networkx as nx
import matplotlib.pyplot as plt
import sys


def main():
    G = nx.DiGraph()

    form_to = [
            ["idle", ["scan"]],
            ["scan", ["idle", "classify"]],
            ["classify", ["grip"]],
            ["grip", ["evaluate"]],
            ["evaluate", ["scan", "trash", "transport blue", "transport red" ]],
            ["trash", ["scan"]],
            ["transport blue", ["detach"]],
            ["transport red", ["detach"]],
            ["detach", ["scan"]],
            ["detach", ["evaluate"]],
        ]

    for indices in form_to:
        from_idx, to_idx_tuple = indices
        G.add_node(from_idx)
        for to_idx in to_idx_tuple:
            #print("from: ",from_idx,"to: ",to_idx)
            G.add_edge(from_idx,to_idx)
            G[from_idx][to_idx]['weight']=1
            #print("edge weight: ",G.get_edge_data(from_idx, to_idx))


    H = nx.DiGraph(G)
    nx.draw_circular(H, with_labels=True, font_weight='bold')

    print(nx.dijkstra_path(G, sys.argv[1], sys.argv[2]))

    plt.show()

if __name__ == "__main__":
    main()