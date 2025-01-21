from langchain_ollama import OllamaLLM

# Load the model
llm = OllamaLLM(model="llama3:8b")
llm.temperature = 0.0

def llm_invoke(template):
    print("Prompting LLM...")
    response = llm.invoke(template)
    return response