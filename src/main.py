"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .recommender import load_songs, recommend_songs, STRATEGIES
except ImportError:
    from recommender import load_songs, recommend_songs, STRATEGIES


def print_recommendations_table(recommendations, user_prefs, strategy: str = "balanced", max_score: float = 8.0) -> None:
    headers = ["#", "Title", "Artist", "Score", "Why"]
    rows = [
        [
            str(i),
            song["title"],
            song["artist"],
            f"{score:.2f} / {max_score:.2f}",
            explanation,
        ]
        for i, (song, score, explanation) in enumerate(recommendations, start=1)
    ]

    # --- tabulate drop-in (pip install tabulate, then uncomment) ---
    # from tabulate import tabulate
    # print(tabulate(rows, headers=headers, tablefmt="simple"))
    # return

    # ASCII fallback — no dependencies required
    col_widths = [len(h) for h in headers]
    for row in rows:
        for j, cell in enumerate(row):
            col_widths[j] = max(col_widths[j], len(cell))

    fmt = "  ".join(f"{{:<{w}}}" for w in col_widths)
    divider = "  ".join("-" * w for w in col_widths)

    strategy_desc = STRATEGIES[strategy]["description"]
    profile_str = f"{user_prefs['genre']} / {user_prefs['mood']} / energy {user_prefs['energy']}"
    print(f"\nTop {len(recommendations)} recommendations for: {profile_str}")
    print(f"Strategy: {strategy}  ({strategy_desc})\n")
    print(fmt.format(*headers))
    print(divider)
    for row in rows:
        print(fmt.format(*row))


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    # Change this to switch ranking strategy:
    # Options: "balanced" | "genre-first" | "mood-first" | "energy-focused"
    STRATEGY = "balanced"

    recommendations = recommend_songs(user_prefs, songs, k=5, strategy=STRATEGY)
    print_recommendations_table(recommendations, user_prefs, strategy=STRATEGY)


if __name__ == "__main__":
    main()
