# 🎧 Model Card: TuneTribe RAG Recommender System

providing transparent documentation on the capabilities, limitations, and ethical considerations of the TuneTribe AI system.

---

## 1. Model Details
* **Model Name:** TuneTribe RAG System (Retrieval-Augmented Generation)
* **Architecture:** The system is an orchestrator rather than a standalone trained model. It utilizes a RAG pipeline combining:
  * **Retriever:** ChromaDB vector database using Google's `gemini-embedding-2`.
  * **Generator:** Google's `gemini-2.5-flash` Large Language Model.
* **Date:** April 2026
* **Version:** 1.0

## 2. Intended Use
* **Primary Use Case:** Recommending music to users by taking a single seed track (e.g., "Songs like Summer Days") and retrieving the most semantically similar tracks from a local listening history database. The system then generates a natural language explanation bridging the user's history with their new request.
* **Out-of-Scope Uses:** This system is not intended for high-stakes decision-making, mental health diagnosis (e.g., inferring depression from sad music requests), or commercial gatekeeping of artist discovery.

## 3. Factors, Biases, and Ethical Considerations (Mitchell, 2018)
* **Demographic Factors:** The system does not explicitly capture user demographic data (age, gender, location). However, music taste is highly correlated with demographics, meaning the AI might implicitly lean toward Western-centric recommendations due to the underlying pre-training of the Gemini model.
* **Dataset Bias:** Because the system operates via RAG, its worldview is strictly limited to the 50 tracks currently stored in the database. If the database lacks international music or niche genres, the system structurally biases against those artists, making them un-discoverable.
* **Popularity Bias:** The underlying Gemini 2.5 Flash model inherently favors popular, globally recognized tracks. If an indie track from the database is mathematically the best fit, the LLM might still attempt to hallucinate a connection to a more famous artist.
* **Commercial / Ethical Misuse:** There is an ethical risk of "payola" (record labels paying to artificially boost their artists). If the underlying vector database is maliciously manipulated to alter the metadata of specific songs, the AI will confidently recommend those artists under false pretenses. Transparent retrieval rules are required to prevent this.

## 4. Training Data & Experimental Info
* **Pre-Trained Models:** The system relies on Google's `gemini-2.5-flash` and `gemini-embedding-2`. Information regarding the billions of parameters and vast web datasets used to train these base models can be found in Google's official model documentation. No fine-tuning was performed.
* **Retrieval Dataset (RAG Context):** The specific dataset powering the recommendations is `data/songs.csv`. This is a small, manually curated dataset of 50 tracks containing metadata such as Title, Artist, Genre, Mood, Energy, Tempo, and Valence. 
* **Experimental Params:** The embeddings were processed using default ChromaDB L2 distance metrics. Batch sizes for embedding were capped at 100 to adhere to API rate limits.

## 5. Evaluation Results
Because music recommendation is highly subjective, the system implements an autonomous **Confidence Scoring** framework for evaluation:
* **Contextual Coherence:** When retrieving tracks within logically adjacent genres (e.g., bridging Surf Rock with Reggae), the model evaluates itself with high confidence (**85% - 95%**) and outputs clear, music-theory-backed justifications (e.g., "both utilize laid-back tempos and off-beat skanking rhythms").
* **Edge-Case Handling:** When presented with illogical pairings (e.g., bridging Classical Piano with Heavy Metal), the system correctly throttles its Confidence Score down to **<40%** and explicitly warns the user that the musical gap is too wide to form a natural bridge.
* **API Reliability:** Initial experimental tracking revealed a 100% failure rate (404 errors) when utilizing the deprecated `google-generativeai` SDK. Migrating to the modern `google-genai` SDK and updating the embedding models resolved these issues entirely.
