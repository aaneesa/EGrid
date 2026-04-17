from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def get_policy_guidelines(query: str):
    """
    Retrieves the top 3 most relevant technical protocols based on a query.
    """
    persist_dir = 'src/vectordb/chroma_db'
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Load the existing database
    db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    
    # Perform Similarity Search
    docs = db.similarity_search(query, k=3)
    
    # Combine content for the Agent's prompt
    context = "\n---\n".join([doc.page_content for doc in docs])
    return context

if __name__ == "__main__":
    # Test it
    test_query = "What is the trigger for critical expansion?"
    print(f"🔍 Searching for: {test_query}")
    print(get_policy_guidelines(test_query))