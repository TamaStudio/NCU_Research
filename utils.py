import nltk

nltk.download('punkt_tab')
nltk.download('words')

from nltk.corpus import words
from nltk.tokenize import sent_tokenize, word_tokenize
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification, AutoModelForSeq2SeqLM

#Named Entity Recognition
def ner(model, text):
    print(f'model: {model}')
    print(f'text: {text}')
    if model=="spacy":
        nlp = spacy.load("en_core_web_trf")
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return (entities)
    elif model=="HFT":
        model_name = "dslim/bert-base-NER"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForTokenClassification.from_pretrained(model_name)
        nlp = pipeline("ner", model=model, tokenizer=tokenizer)
        entities = nlp(text)
        for entity in entities:
            print(f"entity: {entity['word']}")
            return (entity['word'])

# Exract relaions usingdependency parsing
def extract_relations(text):
    nlp = spacy.load("en_core_web_trf")
    doc = nlp(text)
    relations = []
    dependency_label_mapping = {
        "nsubj": "subject_of",
        "dobj": "object_of",
        "attr": "is_attribute_of",
        "prep": "has_preposition",
        "amod": "describes",
        "advmod": "modifies"
    }
    for token in doc:
        if token.dep_ in dependency_label_mapping:  # Simplified relation extraction
            relation = (token.head.text, dependency_label_mapping[token.dep_], token.text)
            relations.append(relation)
    return relations

#Named Entity Linking
def nel(model, text):
    print(f'model: {model}')
    print(f'text: {text}')
    if model=="HFT":
        model_name = "facebook/blink-ner-linking"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        input = tokenizer(text, return_tensors="pt")
        return input

#Processing All PDF File
def process_pdfs_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDF files in {input_folder}. Start processing...")

    for filename in tqdm(pdf_files, desc="Processing PDFs", unit="file"):
        pdf_path = os.path.join(input_folder, filename)
        print(f"Processing {filename}...")

        text = extract_pdf(pdf_path)
        cleaned_text = cleaning_extracted_pdf(text)

        # Tokenize and extract entities
        sentences, words = tokenize_text(cleaned_text)
        entities = ner("spacy", cleaned_text)

        # Extract relations from text
        relations = extract_relations(cleaned_text)

        # Build knowledge graph
        G = build_knowledge_graph(entities, relations)

        # Visualize the graph (optional)
        visualize_graph(G)

        output_graph = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.graphml")
        nx.write_graphml(G, output_graph)

        output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(''.join(sentences) + "\n\n" + ''.join(str(val) for val in entities))



        print(f"Saved to {output_file}")








