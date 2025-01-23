import os
import networkx as nx
import matplotlib.pyplot as plt
import re
import llm
import prompt
import knowledge_graph
import pdf_reader
from langchain_core.prompts import PromptTemplate

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

def extract_entity_and_relation(extracted_text):
    template = PromptTemplate(input_variables=["text"], template=prompt.ner_prompt_template)
    template_prompt = template.format(text=extracted_text)
    entity = llm.llm_invoke(template_prompt)
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(entity)
    return entity

def parse_entity_and_relation():
    # Read the content of output.txt
    with open('output.txt', 'r') as file:
        text = file.read()

    # Define regex patterns to match nodes and edges
    node_pattern = re.compile(r'\((\d+),\s*"([^"]+)",\s*"([^"]+)"\)')
    edge_pattern = re.compile(r'\((\d+),\s*(\d+),\s*"([^"]+)"\)')

    # Parse Nodes
    nodes_matches = node_pattern.findall(text)
    Nodes = [(match[0], match[1], match[2]) for match in nodes_matches]

    # Parse Edges
    edges_matches = edge_pattern.findall(text)
    Edges = [
        (match[0], match[1], match[2]) for match in edges_matches
    ]

    print("Nodes:", Nodes)
    print("Edges:", Edges)
    return Nodes, Edges

def create_knowledge_graph(entity, relation):
    kg_output_path = "kg_result_path"
    G = knowledge_graph.build_knowledge_graph(entity, relation)
    knowledge_graph.visualize_graph(G, kg_output_path)
    return G

def Create_PDF_KG():
    #text = pdf_reader.read_pdf()
    #entity = extract_entity_and_relation(text)
    entity, relation = parse_entity_and_relation()
    G = create_knowledge_graph(entity, relation)
    knowledge_graph.save_graph_to_image(G, "knowledge_graph.png")
    #print(entity)