import chromadb
from chromadb.utils import embedding_functions
import os

# --- PART 1: RAG ENGINE LOGIC ---
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
        ids=[f"id_{user_id}_{reason[:5]}"]
    )
    print(f"✅ Stored Success: {reason}")

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

def validate_leave_request(user_reason):
    # Similarity search pannu
    past_record = get_recommendation(user_reason)
    
    if past_record:
        print(f"\n💡 AI Suggestion: Similar to '{past_record['similar_reason']}'")
        print(f"✅ Usually approved for: {past_record['suggested_duration']} ({past_record['recommended_type']})")
        return past_record
    else:
        print("\nℹ️ New reason detected. Adding to knowledge base...")
        return None

# --- PART 2: TESTING LOGIC (Single Block Only) ---
if __name__ == "__main__":
    print("--- Running RAG System ---")
    
    # 1. Sample data store pannuvom (First time mattum)
    store_leave_history("Suffering from viral fever and headache", "Sick Leave", "3 days", "emp01")
    store_leave_history("Attending my sister's wedding ceremony", "Casual Leave", "2 days", "emp02")

    # 2. Testing Validation
    print("\nTesting Validation for: 'I have a high fever'")
    validate_leave_request("I have a high fever")
    
    print("\nTesting Validation for: 'Going to a family function'")
    validate_leave_request("Going to a family function")