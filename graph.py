import argparse
import networkx as nx
import matplotlib.pyplot as plt
import sys


def main():
    

    G = nx.DiGraph()

    form_to = [
            ["idle", ["scan", "fail"]],
            ["scan", ["idle", "classify", "fail"]],
            ["classify", ["grip", "fail"]],
            ["grip", ["evaluate", "fail"]],
            ["evaluate", ["scan", "trash", "transport blue", "transport red", "fail" ]],
            ["trash", ["scan", "fail"]],
            ["transport blue", ["detach", "fail"]],
            ["transport red", ["detach", "fail"]],
            ["detach", ["scan", "fail"]],
            ["detach", ["evaluate", "fail"]],
            ["fail", ["malfunction_service"]],
            ["malfunction_service", ["idle", "scan", "classify", "grip",
                                     "evaluate", "trash", "transport blue",
                                     "transport red", "detach"]]
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

    if len(sys.argv)==1:
        print("just graph")
        print("to display path add start_node and end_node arguments")
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('start_node', type=str)
        parser.add_argument('end_node', type=str)
        args = parser.parse_args()
        print(nx.dijkstra_path(G, sys.argv[1], sys.argv[2]))

    plt.show()

if __name__ == "__main__":
    main()