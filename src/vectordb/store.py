import os
import chromadb
from chromadb.config import Settings

DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "documents")
PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_store")

def get_chroma_client():
    """Get or create a persistent Chroma client."""
    return chromadb.PersistentClient(path=PERSIST_DIR)

def get_or_create_collection(client=None):
    """Get or create the EGrid planning guidelines collection."""
    if client is None:
        client = get_chroma_client()
    return client.get_or_create_collection(
        name="egrid_planning_guidelines",
        metadata={"description": "EV infrastructure planning guidelines and protocols"}
    )

def chunk_document(text, chunk_size=500, overlap=100):
    """Split a document into overlapping chunks for better retrieval."""
    sentences = text.split(". ")
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)
        if current_length + sentence_length > chunk_size and current_chunk:
            chunks.append(". ".join(current_chunk) + ".")
            # Keep overlap
            overlap_sentences = []
            overlap_length = 0
            for s in reversed(current_chunk):
                if overlap_length + len(s) > overlap:
                    break
                overlap_sentences.insert(0, s)
                overlap_length += len(s)
            current_chunk = overlap_sentences
            current_length = overlap_length
        current_chunk.append(sentence)
        current_length += sentence_length

    if current_chunk:
        chunks.append(". ".join(current_chunk))

    return chunks

def ingest_documents():
    """Read all markdown documents from the documents directory and store them in ChromaDB."""
    client = get_chroma_client()
    
    # Delete existing collection to re-ingest fresh
    try:
        client.delete_collection("egrid_planning_guidelines")
    except Exception:
        pass
    
    collection = get_or_create_collection(client)

    if not os.path.exists(DOCUMENTS_DIR):
        print(f"❌ Documents directory not found: {DOCUMENTS_DIR}")
        return

    doc_files = [f for f in os.listdir(DOCUMENTS_DIR) if f.endswith(".md")]

    if not doc_files:
        print("❌ No markdown documents found to ingest.")
        return

    all_ids = []
    all_documents = []
    all_metadatas = []

    for doc_file in doc_files:
        filepath = os.path.join(DOCUMENTS_DIR, doc_file)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Chunk the document for granular retrieval
        chunks = chunk_document(content)
        source_name = doc_file.replace(".md", "").replace("_", " ").title()

        for i, chunk in enumerate(chunks):
            doc_id = f"{doc_file}__chunk_{i}"
            all_ids.append(doc_id)
            all_documents.append(chunk)
            all_metadatas.append({
                "source": doc_file,
                "source_name": source_name,
                "chunk_index": i,
                "total_chunks": len(chunks)
            })

    collection.add(
        ids=all_ids,
        documents=all_documents,
        metadatas=all_metadatas
    )

    print(f"✅ Ingested {len(all_ids)} chunks from {len(doc_files)} documents:")
    for doc_file in doc_files:
        count = sum(1 for m in all_metadatas if m["source"] == doc_file)
        print(f"   📄 {doc_file} → {count} chunks")

def retrieve(query, n_results=5):
    """Retrieve relevant document chunks for a query."""
    collection = get_or_create_collection()
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    retrieved = []
    if results and results["documents"]:
        for i, doc in enumerate(results["documents"][0]):
            retrieved.append({
                "content": doc,
                "source": results["metadatas"][0][i]["source_name"],
                "source_file": results["metadatas"][0][i]["source"],
                "distance": results["distances"][0][i] if results.get("distances") else None
            })
    
    return retrieved

if __name__ == "__main__":
    ingest_documents()
    
    # Test retrieval
    print("\n--- Test Retrieval ---")
    test_queries = [
        "What should I do when Load_Score is above 70?",
        "How to handle charging in cold weather?",
        "What is the pricing strategy for peak hours?"
    ]
    for q in test_queries:
        print(f"\n🔍 Query: {q}")
        results = retrieve(q, n_results=2)
        for r in results:
            print(f"   📌 [{r['source']}] {r['content'][:120]}...")
