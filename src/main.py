"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False},
        "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
        "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.95, "likes_acoustic": False},
        "Conflicted: sad but hyped": {"genre": "edm", "mood": "sad", "energy": 0.95, "likes_acoustic": False},
        "No matches anywhere": {"genre": "country", "mood": "angry", "energy": 0.5, "likes_acoustic": True},
    }

    for name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print(f"\n=== {name} ===  {user_prefs}\n")
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} — {song['artist']}  [score: {score:.2f}]")
            print(f"   why: {explanation}\n")



if __name__ == "__main__":
    main()
