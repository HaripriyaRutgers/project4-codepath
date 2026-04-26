import pandas as pd
import logging
import os

# Configure logging to print out to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_music_data(filepath="data/songs.csv"):
    """
    Reads the music history CSV and combines title, artist, and genre into a metadata column.
    """
    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}. Please ensure the file exists.")
        return None
        
    try:
        # Read the CSV
        df = pd.read_csv(filepath)
        
        # Check if required columns exist
        required_cols = ['title', 'artist', 'genre']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logging.error(f"Missing required columns in CSV: {missing_cols}")
            return None
            
        # Combine columns into a 'metadata' string
        df['metadata'] = df['title'] + " by " + df['artist'] + " [Genre: " + df['genre'] + "]"
        
        # Log the successful load
        logging.info(f"Successfully loaded {len(df)} songs from {filepath}")
        
        return df
        
    except Exception as e:
        logging.error(f"An error occurred while reading the file: {e}")
        return None

if __name__ == "__main__":
    # Test the loader
    df = load_music_data("data/songs.csv")
    
    if df is not None and not df.empty:
        print("\nSample of combined metadata:")
        print(df['metadata'].head().tolist())
