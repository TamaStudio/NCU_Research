import os
import re
import llm
import prompt
import knowledge_graph
import drm
#import wiki
from langchain_core.prompts import PromptTemplate

pdf_source_path = "pdf_source"
pdf_extract_result_path = "pdf_extract_result_path"
kg_result_path = "kg_result_path"
input_question = "What the difference between IoT and XoT?"
clues = ""
pruned_question_entities = ""
topic_entities = []


def initialization():
     #Find and Prune Topic entities
    template = PromptTemplate(input_variables=["question"], template=prompt.question_ner_and_prune)
    template_prompt = template.format(question=input_question)
    pruned_question_entities = llm.llm_invoke(template_prompt)
    topic_entities_pattern = re.compile(r'"*([^"]+)", "*([^"]+)"\]')
    topic_entities_matches = topic_entities_pattern.findall(pruned_question_entities)
    topic_entities = [(match) for match in topic_entities_matches]
    
    #Find chunk from documents using DRM dual-tower model
    documents = []
    for filename in os.listdir(pdf_extract_result_path):
        if filename.endswith(".txt"):
            documents_path = os.path.join(pdf_extract_result_path, filename)
            with open(documents_path, 'r', encoding='utf-8') as file:
                documents.append(file.read())

    chunks =  drm.Dense_Retrieval(input_question, documents) 

    #Evaluates the sufficieny of knowledge to answer the question
    reasoning_template = PromptTemplate(input_variables=["question", "clue", "chunk"], template=prompt.initialize_reasoning)
    reasoning_template_prompt = reasoning_template.format(question=input_question, clue=clues, chunk=chunks)
    reasoning_result = llm.llm_invoke(reasoning_template_prompt)
    print(reasoning_result)

if __name__ == "__main__":
    #pdf_reader.read_pdf(pdf_source_path, pdf_extract_result_path)
    #knowledge_graph.Create_PDF_KG()
    initialization()
