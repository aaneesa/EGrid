from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.tools import tool
import os

_db = None

def _get_db():
    """Lazy-loads the Chroma DB only when first called, preventing macOS segfault on import."""
    global _db
    if _db is None:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        persist_dir = os.path.join(BASE_DIR, "vectordb", "chroma_db")
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        _db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return _db

@tool
def policy_researcher(query: str):
    """
    Searches the technical protocol database for EV grid mandates, RERA rules, 
    and engineering guidelines. Use this tool when you need to cite specific 
    Protocol IDs (like GS-CRIT-03) or find legal/technical constraints.
    """
    db = _get_db()
    docs = db.similarity_search(query, k=3)
    context = "\n---\n".join([doc.page_content for doc in docs])
    return context

if __name__ == "__main__":
    test_query = "What is the trigger for critical expansion?"
    print(policy_researcher.run(test_query))