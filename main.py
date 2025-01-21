import os
import re
import llm
import prompt
import pdf_reader
import knowledge_graph
from langchain_core.prompts import PromptTemplate

clues = ""
topic_entity = []


def read_pdf():
    # Processing PDF
    pdf_input_path = "source"
    pdf_output_path = "result"
    result = pdf_reader.process_pdfs_in_folder(pdf_input_path, pdf_output_path)
    return result

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
    kg_output_path = "result"
    G = knowledge_graph.build_knowledge_graph(entity, relation)
    knowledge_graph.visualize_graph(G, kg_output_path)
    return G

def Create_PDF_KG():
    #text = read_pdf()
    #entity = extract_entity_and_relation(text)
    entity, relation = parse_entity_and_relation()
    G = create_knowledge_graph(entity, relation)
    knowledge_graph.save_graph_to_image(G, "knowledge_graph.png")
    #print(entity)

if __name__ == "__main__":
    Create_PDF_KG()