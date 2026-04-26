# 🎵 AI-Powered Music Recommender (RAG System)

## The Original Project: Rule-Based Simulation
Originally, this project was a "Music Recommender Simulation" (built during earlier modules). Its goal was to represent songs and user taste profiles as structured data and use hardcoded, mathematical scoring rules (e.g., adding points for matching genres or energy levels) to rank and recommend songs. While effective as a baseline, it lacked the ability to understand semantic nuances, musical context, or user intent beyond rigid formulas.

## Project Summary
This upgraded project transforms that rigid rule-based engine into an intelligent **Retrieval-Augmented Generation (RAG) Chatbot**. 

Instead of relying on hardcoded math, the system stores a diverse catalog of songs in a local Vector Database. When a user asks for a recommendation based on a specific song, the system retrieves their most relevant listening history and provides it as context to a Large Language Model (LLM). The AI then synthesizes this data to recommend a new song that perfectly bridges their tastes, explaining *why* it fits in natural language. This matters because it creates a highly personalized, conversational, and intuitive discovery experience for the user.

---

## 🏗️ Architecture Overview

The system is built on a modern RAG architecture:
1. **Data Ingestion (`data_loader.py` & `vector_store.py`)**: The system parses a CSV catalog of songs, formats them into descriptive text, and converts them into mathematical vectors using Google's `gemini-embedding-2` model. These are stored locally in **ChromaDB**.
2. **Retrieval (`app.py`)**: When the user enters a song query, the app searches ChromaDB for the 3 most semantically similar songs from the database to represent relevant listening history.
3. **Generation (`app.py`)**: A dynamic prompt is constructed combining the user's query and the retrieved history. This is sent to Google's **`gemini-2.5-flash`** LLM, which generates the final, personalized recommendation.

![System Architecture](assets/system_architecture.png)
*(Ensure you have exported the Mermaid diagram to your assets folder!)*

---

## 🚀 Setup Instructions

1. **Clone the repository** and navigate to the project directory.
2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```
3. **Set up your API Key**:
   Create a file named `.env` in the root directory and add your Google Gemini API key:
   ```text
   GEMINI_API_KEY=your_api_key_here
   ```
4. **Initialize the Vector Database**:
   Run the following script to embed the song catalog into ChromaDB. (You only need to do this once, or whenever the CSV updates).
   ```bash
   python3 src/vector_store.py
   ```
5. **Run the Chatbot**:
   ```bash
   python3 src/app.py
   ```

---

## 💬 Sample Interactions

**Input 1:**
> 🎵 Ask for songs like a specific track: **Summer Days**

**AI Output:**
> [🔍 Searching your listening history...]
> Found 3 similar songs from your history:
>   - Summer Days by Beach Bums [Genre: surf rock]
>   - Ocean Breeze by Waveform [Genre: reggae]
>   - Island Time by Coconut Crew [Genre: reggae]
> 
> ✨ RECOMMENDATION ✨
> The user enjoys both the energetic sounds of surf rock ("Summer Days") and the laid-back rhythms of reggae. 
> **Suggested Song:** "Pipeline Pulse" by The Salty Skankers
> **Why:** It seamlessly blends the upbeat, adventurous spirit of surf rock with a chill, head-nodding reggae groove. The twangy, reverb-drenched guitar melody evokes classic surf rock, while the rhythm section kicks in with a clear, laid-back skanking reggae rhythm.

**Input 2:**
> 🎵 Ask for songs like a specific track: **Sunrise City**

**AI Output:**
> [🔍 Searching your listening history...]
> Found 3 similar songs from your history:
>   - Sunrise City by Neon Echo [Genre: pop]
>   - Neon Sunrise by Synth Magic [Genre: synthwave]
>   - City Lights by Urban Flow [Genre: r&b]
>
> ✨ RECOMMENDATION ✨
> **Suggested Song:** "Midnight Drive" by The Neon Syndicate
> **Why:** This song perfectly bridges the upbeat, catchy nature of pop with the retro-futuristic, electronic atmosphere of synthwave. It features the driving bassline you love in "Sunrise City", but wraps it in the moody, shimmering synthesizers found in "Neon Sunrise", creating a perfect late-night driving anthem.

---

## 🧠 Design Decisions & Trade-offs

* **RAG over Fine-Tuning:** I chose to use a RAG approach rather than fine-tuning a model. Fine-tuning is expensive, time-consuming, and difficult to update. RAG allows the database (the CSV catalog) to be updated instantly without ever retraining the AI.
* **Local ChromaDB vs. Cloud Vector DB:** I utilized a persistent local Chroma database rather than a hosted solution like Pinecone. While a cloud DB scales better for millions of users, a local DB removes latency, eliminates cloud costs, and makes the project entirely self-contained for portfolio demonstration.
* **Simulated History:** As a trade-off for simplicity, the "user history" is currently simulated by retrieving the nearest neighbors of the inputted song from the static CSV. In a production environment, this would be hooked up to an actual user-profile database logging their chronological listens.

---

## 🧪 Testing Summary

* **What worked:** The semantic retrieval is incredibly powerful. ChromaDB successfully identified the nuanced similarities between tracks based on their metadata strings. Gemini 2.5 Flash proved highly capable of taking disparate genres (like Surf Rock and Reggae) and hallucinating highly logical, creative "bridge" songs.
* **What didn't work initially:** I ran into significant versioning issues with the Google Generative AI Python SDKs. Older SDKs and deprecated models (`text-embedding-004` and `gemini-1.5-flash`) threw 404 errors. 
* **How it was fixed:** I refactored the entire system to use the modern `google-genai` library, implementing a custom embedding class to ensure ChromaDB natively utilized `gemini-embedding-2`, ensuring the system is fully future-proofed for 2026 standards.

---

## 🪞 Reflection

Building this system fundamentally shifted my perspective on AI from a "magic black box" to an orchestratable tool. I learned that an LLM is only as smart as the context you provide it. Instead of feeding a model a massive, expensive prompt with an entire catalog of music, RAG taught me how to surgically inject only the most relevant, targeted information. 

This project reinforced that successful AI problem-solving is less about writing perfect algorithms, and more about designing clever data pipelines that connect the right information to the right model at the right time.
