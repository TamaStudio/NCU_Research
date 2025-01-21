import os
import networkx as nx
import matplotlib.pyplot as plt

# Create a Knowledge Graph using NetworkX
def build_knowledge_graph(entities, relations):
    G = nx.Graph()

    # Add nodes for each entity
    for entity in entities:  
        G.add_node(entity[0], label=entity[2])  # Entity text and type

    # Add edges for each relation
    for relation in relations:
        G.add_edge(relation[0], relation[1], label=relation[2])  # Head -> Dependent with relation

    return G

# Visualize the Knowledge Graph and save it as an image
def save_graph_to_image(G, filename="knowledge_graph.png"):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G)  # Layout for nodes
    
    # Draw the components of the graph
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="skyblue")
    nx.draw_networkx_labels(G, pos, font_size=12)
    nx.draw_networkx_edges(G, pos, width=2)

    # Set title
    plt.title("Knowledge Graph")
    
    # Save the graph to an image file
    plt.savefig(filename, format="PNG")  # You can change the format to PNG, PDF, etc.
    plt.close()  # Close the plot to avoid showing it in non-interactive environments
    
# Visualize the Knowledge Graph using matplotlib
def visualize_graph(G, kg_output_path):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G)  # Layout for nodes
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="skyblue")
    nx.draw_networkx_labels(G, pos, font_size=12)
    nx.draw_networkx_edges(G, pos, width=2)
    plt.title("Knowledge Graph")
    plt.show()
    output_graph = os.path.join(kg_output_path, f"KG.graphml")
    nx.write_graphml(G, output_graph)