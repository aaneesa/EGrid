import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def build_egrid_knowledge_base():
    # 1. Setup paths
    docs_dir = 'data/guidelines/' 
    persist_dir = 'src/vectordb/chroma_db'
    
    print("🚀 Initializing EGrid RAG Ingestion...")

    # 2. Load all Markdown files
    if not os.path.exists(docs_dir) or not os.listdir(docs_dir):
        print(f" Error: Place your .md files in {docs_dir} first!")
        return

    loader = DirectoryLoader(docs_dir, glob="./*.md", loader_cls=TextLoader)
    documents = loader.load()
    print(f"Loaded {len(documents)} core policy documents.")

    # 3. Smart Chunking
    # We use 700 chars to keep tables and Protocol IDs together
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, 
        chunk_overlap=100,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split policies into {len(chunks)} searchable technical chunks.")

    # 4. Generate Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 5. Create and Persist Vector Store
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    
    print(f"SUCCESS: Knowledge Base built at {persist_dir}")

if __name__ == "__main__":
    build_egrid_knowledge_base()