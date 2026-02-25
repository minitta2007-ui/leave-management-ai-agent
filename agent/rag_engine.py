import chromadb
from chromadb.utils import embedding_functions
import os

# Database folder
db_path = "./chroma_db"
if not os.path.exists(db_path):
    os.makedirs(db_path)

client = chromadb.PersistentClient(path=db_path)
model_name = "all-MiniLM-L6-v2"
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)

collection = client.get_or_create_collection(
    name="leave_history",
    embedding_function=embedding_fn
)

def store_leave_history(reason, leave_type, duration, user_id):
    collection.add(
        documents=[reason],
        metadatas=[{"leave_type": leave_type, "duration": duration}],
        ids=[f"id_{user_id}"]
    )
    print(f"Stored: {reason}")

def get_recommendation(query_reason):
    results = collection.query(
        query_texts=[query_reason],
        n_results=1
    )
    if results['documents'] and len(results['documents'][0]) > 0:
        return {
            "similar_reason": results['documents'][0][0],
            "recommended_type": results['metadatas'][0][0]['leave_type'],
            "suggested_duration": results['metadatas'][0][0]['duration']
        }
    return None