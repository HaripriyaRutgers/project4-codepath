# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.


Real-world recommendation systems, like those used by Spotify or YouTube, analyze both user preferences and item attributes to suggest personalized content. They often combine collaborative filtering (using data from similar users) and content-based filtering (matching items to a user's past preferences). In this simulation, our system will prioritize **content-based filtering**, focusing on matching songs to user preferences based on their attributes.

### Features Used:
- **Song**: Each `Song` will use the following features: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.
- **UserProfile**: The `UserProfile` will store preferences for `fav_genre`, `fav_mood`, and numerical ranges for `target_energy`, `tempo_bpm`, and other relevant features.

The recommender will compute a score for each song by comparing its attributes to the user's preferences, rewarding songs that are closer to the desired values. The top-scoring songs will be recommended to the user.


### Algorithm Recipe

The recommendation system works by scoring each song in the dataset based on how well it matches the user's preferences. The process is as follows:

1. **Input**: The user provides their preferences:
   - `fav_genre`: Preferred genre.
   - `fav_mood`: Preferred mood.
   - `target_energy`: Desired energy level (a value between 0 and 1).

2. **Processing**:
   - For each song in the dataset:
     1. **Genre Match**: If the song's genre matches the user's preferred genre, add **3.0 points**.
     2. **Mood Match**: If the song's mood matches the user's preferred mood, add **2.0 points**.
     3. **Energy Similarity**: Calculate the energy similarity score using the formula:
        ```math
        Energy Score = 5.0 * (1 - |song_energy - target_energy|)
        ```
        - A perfect energy match gives the full 5.0 points, while larger differences reduce the score linearly.

3. **Output**:
   - After processing all songs, sort them by their total score in descending order.
   - Return the top K songs as recommendations.

   

### Potential Biases

While this system is designed to prioritize user preferences, there are some potential biases to consider:
- **Genre Over-Prioritization**: The system heavily weights genre matches (+3.0 points), which might cause it to overlook songs with excellent mood or energy matches but from different genres.
- **Energy Sensitivity**: The energy similarity score is linear, which may not reflect how users perceive energy differences (e.g., small differences might feel negligible to users).
- **Limited Context**: The system does not account for collaborative filtering (e.g., what similar users like), which could limit its ability to recommend songs outside the user's stated preferences.

By understanding these biases, future iterations of the system can incorporate additional techniques (e.g., collaborative filtering or user feedback loops) to improve recommendation quality.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

