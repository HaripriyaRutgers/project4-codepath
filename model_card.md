# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  

TuneTribe

---

## 2. Intended Use  

TuneTribe recommends songs from a small catalog based on three things: your favorite genre, your preferred mood, and how energetic you want the music to feel. It assumes you can describe your taste in simple terms — there is no listening history or rating system. This is a classroom project, not a real app, so the catalog is small and the logic is intentionally simple enough to read and understand.

---

## 3. How the Model Works  

Every song in the catalog gets a score based on how well it matches what you asked for across three signals: genre, mood, and energy. Genre and mood are binary — you either match or you don't, no partial credit. Energy uses a sliding scale where a perfect match earns the full points and the score drops the further away the song is.

The model now supports four ranking strategies. Each one uses the same three signals but shifts how much each one matters:

- **Balanced** — the default. Genre is worth 3 points, mood is currently turned off, energy up to 5. Max score is 8.
- **Genre-First** — genre jumps to 6 points. Energy drops to 3 max. Good for users who refuse to leave their genre no matter what.
- **Mood-First** — mood jumps to 6 points. Energy drops to 3 max. Good for users who care more about feel than genre label.
- **Energy-Focused** — energy is worth up to 8 points. Genre and mood are each worth just 1. Good for workout playlists or background music where vibe matters more than category.

You switch strategies by changing one line in `main.py`. Every recommendation still shows the exact point breakdown so you can see how the strategy affected the result.

---

## 4. Data  

The catalog has 20 songs across 17 genres, including pop, lofi, rock, jazz, EDM, metal, folk, classical, and disco. Energy levels range from 0.20 (very quiet) to 0.97 (very loud). Moods include happy, chill, intense, calm, moody, and about a dozen others. No songs were added or removed from the starter dataset. Big gaps include genres like soul, R&B, latin, and bossa nova, which have zero songs. Common moods like "sad," "romantic," and "melancholic" also do not appear at all, so users who want those will never get a mood match bonus.

---

## 5. Strengths  

The system works best when a user's genre and energy preferences point in the same direction — for example, an EDM fan who wants high energy will get the EDM song at the top with a near-perfect score. The scoring is completely transparent: every recommendation comes with a printed explanation showing exactly how many points each signal contributed. Having four strategies makes it easy to run the same profile through different modes and immediately see how the rankings shift — for instance, "Gym Hero" scores second under Balanced but drops to third under Mood-First because its mood tag is "intense," not "happy." That kind of comparison is a useful way to understand what the weights are actually doing.

---

## 6. Limitations and Bias 

The energy signal carries the most weight in the scoring formula (up to 5 points), which means it can override a user's genre preference entirely — for example, a metal fan who prefers calm music will be recommended a folk song over their own genre because the energy match scores higher. The catalog also skews heavily toward high-energy songs, with 10 of 20 tracks above 0.65 energy, so users who prefer medium energy have very few close matches and end up receiving songs that were not well-suited to them. Genres outside the 17 represented in the catalog — such as soul, R&B, or latin — receive no genre bonus at all, silently capping those users at a lower maximum score with no warning. The `acousticness` field is collected for every song and users can express an acoustic preference, but neither value is ever used in scoring, making that preference completely invisible to the recommender. Finally, the energy penalty is symmetric, treating "slightly too loud" and "slightly too quiet" as equally bad, even though real listeners often have directional tolerance — someone who likes moderate energy may not mind an energetic song but strongly dislike a lethargic one.

---

## 7. Evaluation  

Five user profiles were tested to check whether the recommender behaved as expected. The first was a straightforward "Happy Pop Fan" who wants upbeat pop music at high energy — this profile worked well, with "Sunrise City" landing at the top as expected. The second was a "Low-Energy Pop Fan" who prefers pop but at a very quiet, mellow level; surprisingly, a classical song ("Golden Hour") ranked above all the pop songs because the energy gap penalty was so steep that the genre bonus could not compensate. The third was a "Calm Metal Fan" who listed metal as their genre but preferred low-energy listening; the only metal song in the catalog ("Firestorm") ranked fourth, beaten by a folk song, a new age song, and a classical song — none of which match the genre at all. The fourth was an "EDM Fan" targeting very high energy, which was the clearest success: the one EDM song in the catalog scored a perfect 8.0, since genre and energy both aligned exactly. The fifth was a "Folk and Acoustic Fan" at low energy, which also worked reasonably well, though the second result was a new age song rather than anything acoustic or folk, because acousticness is not factored into scoring. The most surprising finding overall was how quickly a mismatch in energy could completely erase a genre preference — the system behaved less like a music recommender and more like an energy-level filter whenever the catalog did not have songs that matched both signals at once.

---

## 8. Future Work  

The most useful next step would be to plug in the `acousticness` field, since it is already stored for every song and every user profile has an acoustic preference — the wiring just never got done. Longer term, letting users pick more than one genre would make the recommendations feel much more personal. Adding more songs to fill the middle of the energy range (0.45–0.65 is very thin right now) would also improve results without changing any code. Clamping the energy input to stay between 0 and 1 would prevent the edge case where out-of-range values produce negative scores. It would also be interesting to let users pick a strategy from the command line instead of editing the source file, so switching modes feels more like a feature than a code change.

---

## 9. Personal Reflection  

The biggest thing I learned is that recommender systems are really just a set of priorities written as math — and whichever signal you weight highest ends up running the show. The most surprising moment was seeing a classical song rank above pop songs for a user who asked for pop, just because the energy matched better. It made me realize that Spotify and similar apps must use dozens of signals and huge catalogs specifically to avoid these kinds of gaps, because with only a few signals and 20 songs it is very easy for the wrong song to win for completely logical but unintuitive reasons.
