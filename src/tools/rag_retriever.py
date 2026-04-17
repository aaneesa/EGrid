from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.tools import tool 

# Initialize once at the top to save time/memory
persist_dir = 'src/vectordb/chroma_db'
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load the existing database once
db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)

@tool
def policy_researcher(query: str):
    """
    Searches the technical protocol database for EV grid mandates, RERA rules, 
    and engineering guidelines. Use this tool when you need to cite specific 
    Protocol IDs (like GS-CRIT-03) or find legal/technical constraints.
    """
    # Perform Similarity Search
    docs = db.similarity_search(query, k=3)
    
    # Combine content for the Agent's prompt
    context = "\n---\n".join([doc.page_content for doc in docs])
    return context

if __name__ == "__main__":
    # Test it
    test_query = "What is the trigger for critical expansion?"
    print(policy_researcher.run(test_query)) # Use .run() for testing @tools