from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5, strategy: str = "balanced") -> List[Song]:
        user_prefs = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
        }
        scorer = STRATEGIES[strategy]["scorer"]
        scored = []
        for song in self.songs:
            song_dict = {'genre': song.genre, 'mood': song.mood, 'energy': song.energy}
            score, _ = scorer(user_prefs, song_dict)
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a CSV of songs and return a list of dicts with numeric fields cast to int/float."""
    import csv
    songs = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get('id', '').strip():
                continue
            songs.append({
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences and return (total_score, reasons)."""
    score = 0.0
    reasons = []

    # Genre match: +3.0 points
    if song['genre'] == user_prefs.get('genre'):
        score += 3.0
        reasons.append("genre match (+3.0)")

    # Mood match: +2.0 points (temporarily disabled to observe ranking changes)
    # if song['mood'] == user_prefs.get('mood'):
    #     score += 2.0
    #     reasons.append("mood match (+2.0)")

    # Energy similarity: 5.0 * (1 - |song_energy - target_energy|)
    energy_score = 5.0 * (1 - abs(song['energy'] - user_prefs.get('energy', 0.5)))
    score += energy_score
    reasons.append(f"energy similarity ({energy_score:.2f})")

    return score, reasons

def score_genre_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Genre 6 pts · mood 1 pt · energy up to 3 pts. Max = 10."""
    score = 0.0
    reasons = []
    if song['genre'] == user_prefs.get('genre'):
        score += 6.0
        reasons.append("genre match (+6.0)")
    if song['mood'] == user_prefs.get('mood'):
        score += 1.0
        reasons.append("mood match (+1.0)")
    energy_score = 3.0 * (1 - abs(song['energy'] - user_prefs.get('energy', 0.5)))
    score += energy_score
    reasons.append(f"energy similarity ({energy_score:.2f})")
    return score, reasons


def score_mood_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Mood 6 pts · genre 1 pt · energy up to 3 pts. Max = 10."""
    score = 0.0
    reasons = []
    if song['genre'] == user_prefs.get('genre'):
        score += 1.0
        reasons.append("genre match (+1.0)")
    if song['mood'] == user_prefs.get('mood'):
        score += 6.0
        reasons.append("mood match (+6.0)")
    energy_score = 3.0 * (1 - abs(song['energy'] - user_prefs.get('energy', 0.5)))
    score += energy_score
    reasons.append(f"energy similarity ({energy_score:.2f})")
    return score, reasons


def score_energy_focused(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Energy up to 8 pts · genre 1 pt · mood 1 pt. Max = 10."""
    score = 0.0
    reasons = []
    if song['genre'] == user_prefs.get('genre'):
        score += 1.0
        reasons.append("genre match (+1.0)")
    if song['mood'] == user_prefs.get('mood'):
        score += 1.0
        reasons.append("mood match (+1.0)")
    energy_score = 8.0 * (1 - abs(song['energy'] - user_prefs.get('energy', 0.5)))
    score += energy_score
    reasons.append(f"energy similarity ({energy_score:.2f})")
    return score, reasons


STRATEGIES: Dict[str, Dict] = {
    "balanced":       {"scorer": score_song,           "description": "Genre 3 pts · mood disabled · energy up to 5 pts"},
    "genre-first":    {"scorer": score_genre_first,    "description": "Genre 6 pts · mood 1 pt · energy up to 3 pts"},
    "mood-first":     {"scorer": score_mood_first,     "description": "Mood 6 pts · genre 1 pt · energy up to 3 pts"},
    "energy-focused": {"scorer": score_energy_focused, "description": "Energy up to 8 pts · genre 1 pt · mood 1 pt"},
}


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, strategy: str = "balanced") -> List[Tuple[Dict, float, str]]:
    """Score every song using the chosen strategy, sort by score descending, return top k."""
    scorer = STRATEGIES[strategy]["scorer"]
    scored = [(song, *scorer(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return [(song, score, ", ".join(reasons)) for song, score, reasons in ranked[:k]]
