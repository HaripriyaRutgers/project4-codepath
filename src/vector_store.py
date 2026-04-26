import os
import warnings

# Suppress FutureWarnings from google-auth and urllib3 due to Python 3.9 EOL
warnings.filterwarnings("ignore")

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from google import genai
from dotenv import load_dotenv
from data_loader import load_music_data

class GeminiEmbeddingFunction(EmbeddingFunction):
    """Custom embedding function using the new google-genai SDK."""
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        
    def __call__(self, input: Documents) -> Embeddings:
        # Note: gemini-2.5-flash is for text generation. 
        # For embeddings, we MUST use an embedding model like gemini-embedding-2.
        response = self.client.models.embed_content(
            model="gemini-embedding-2",
            contents=input
        )
        return [e.values for e in response.embeddings]

def init_vector_store(db_path="./chroma_db", collection_name="music_history"):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment.")
        
    client = chromadb.PersistentClient(path=db_path)
    embed_fn = GeminiEmbeddingFunction(api_key=api_key)
    
    # We must delete the old collection because it was using a different embedding model
    # (the default all-MiniLM-L6-v2) and the vector dimensions won't match!
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass
        
    collection = client.get_or_create_collection(name=collection_name, embedding_function=embed_fn)
    return collection

def embed_csv_to_db(filepath="data/songs.csv", db_path="./chroma_db", collection_name="music_history"):
    df = load_music_data(filepath)
    
    if df is None or df.empty:
        raise ValueError("Failed to load data. The CSV file may be missing or empty.")
        
    if 'metadata' not in df.columns or 'id' not in df.columns:
        raise ValueError("The loaded data is missing required columns ('metadata' or 'id').")

    print("Initializing ChromaDB with Gemini Embeddings...")
    collection = init_vector_store(db_path, collection_name)
    
    documents = df['metadata'].tolist()
    ids = [str(song_id) for song_id in df['id'].tolist()]
    metadatas = [
        {"title": row['title'], "artist": row['artist'], "genre": row['genre']} 
        for _, row in df.iterrows()
    ]
    
    try:
        print(f"Embedding {len(documents)} songs using gemini-embedding-2... This may take a few seconds.")
        # We process in batches of 100 to avoid API limits
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            collection.upsert(
                documents=documents[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size],
                ids=ids[i:i+batch_size]
            )
        print(f"Successfully embedded all songs into '{collection_name}' at {db_path}.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while embedding data: {e}")
        
    return collection

if __name__ == "__main__":
    try:
        embed_csv_to_db(filepath="data/songs.csv")
    except Exception as e:
        print(f"Error: {e}")
