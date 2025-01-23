import torch
import torch.nn.functional as F
from transformers import DPRQuestionEncoder, DPRContextEncoder, DPRContextEncoderTokenizer, DPRQuestionEncoderTokenizer

#Load the question encoder and tokenizer
question_encoder = DPRQuestionEncoder.from_pretrained('facebook/dpr-question_encoder-single-nq-base')
question_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained('facebook/dpr-question_encoder-single-nq-base')

#Load the context encode and tokenizer
context_encoder = DPRContextEncoder.from_pretrained('facebook/dpr-ctx_encoder-single-nq-base')
context_tokenizer = DPRContextEncoderTokenizer.from_pretrained('facebook/dpr-ctx_encoder-single-nq-base')

#Devde document into smaller chunks
def chunk_document(document, chunk_size=300):
    words = document.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

#Encode chunks
def Encode_Chunks(chunks):
    chunk_embeddings = []
    for chunk in chunks:
        inputs = context_tokenizer(chunk, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            chunk_embedding = context_encoder(**inputs).pooler_output
        chunk_embeddings.append(chunk_embedding)
    chunk_embeddings = torch.cat(chunk_embeddings, dim=0)
    return chunk_embeddings

#Encode query
def Encode_Query(query):
    inputs = question_tokenizer(query, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        query_embedding = question_encoder(**inputs).pooler_output
    query_embeddings = []
    query_embeddings.append(query_embedding)
    query_embeddings = torch.cat(query_embeddings, dim=0)
    return query_embeddings

#Perform Dense Retrieval
def Dense_Retrieval(query, documents):
    #Encode query
    query_embedding = Encode_Query(query)
 
    #Encode documents
    chunks = []
    for doc in documents:
        chunks.extend(chunk_document(doc))
    chunk_embeddings = Encode_Chunks(chunks)
    
    #Compute similarity scores
    similarity_scores = F.cosine_similarity(query_embedding, chunk_embeddings)
    
    #Get top 5 documents
    top_1_scores, top_1_indices = similarity_scores.topk(3)
    top_1_chunks = [chunks[i] for i in top_1_indices]
    #print (top_1_chunks)
    return top_1_chunks
    