import os
import sys
import warnings

# Suppress FutureWarnings from google-auth and urllib3 due to Python 3.9 EOL
warnings.filterwarnings("ignore")
import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from google import genai
from dotenv import load_dotenv

class GeminiEmbeddingFunction(EmbeddingFunction):
    """Custom embedding function to match what was used to embed the data."""
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        
    def __call__(self, input: Documents) -> Embeddings:
        response = self.client.models.embed_content(
            model="gemini-embedding-2",
            contents=input
        )
        return [e.values for e in response.embeddings]

def init_systems():
    load_dotenv()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: The GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)
        
    # Initialize the new google-genai SDK client
    genai_client = genai.Client(api_key=api_key)
    
    try:
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        embed_fn = GeminiEmbeddingFunction(api_key=api_key)
        collection = chroma_client.get_collection(name="music_history", embedding_function=embed_fn)
    except Exception as e:
        print(f"ERROR: Could not connect to ChromaDB ({e}).")
        print("Ensure you have run 'python3 src/vector_store.py' first to embed the data.")
        sys.exit(1)
        
    return genai_client, collection

def chat_loop():
    genai_client, collection = init_systems()
    
    print("\n" + "="*55)
    print("🎶 Welcome to the RAG-based Music Recommender Bot! 🎶")
    print("Type 'exit' or 'quit' to stop the chatbot.")
    print("="*55 + "\n")
    
    while True:
        try:
            song_x = input("\n🎵 Ask for songs like a specific track: ")
            
            if song_x.strip().lower() in ['exit', 'quit']:
                print("Goodbye! Keep grooving. 👋")
                break
                
            if not song_x.strip():
                continue
                
            print("\n[🔍 Searching your listening history in the Vector DB...]")
            
            results = collection.query(
                query_texts=[song_x],
                n_results=3
            )
            
            documents = results.get('documents', [[]])[0]
            if not documents:
                print("No listening history found to base recommendations on.")
                continue
                
            history_str = "\n".join([f"  - {doc}" for doc in documents])
            print("Found 3 similar songs from your history:\n" + history_str)
            
            prompt = f"""The user likes:
{history_str}

They just asked for songs like: {song_x}.

Respond EXACTLY in this format with NO asterisks, bolding, or markdown formatting:

Recommended Song: [Song Name] by [Artist]
Why: [2-3 sentences explaining the musical bridge between their history and their request]
Confidence Score: [0-100%]
Justification: [1 sentence explaining the confidence score]"""
            print("\n[🧠 Consulting the LLM for a recommendation...]")
            
            # Use gemini-2.5-flash for generation using the new SDK syntax
            response = genai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            print("\n" + "-"*40)
            print(f"✨ RECOMMENDATION ✨")
            print("-"*40)
            print(response.text)
            print("-"*40 + "\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye! Keep grooving. 👋")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    chat_loop()
