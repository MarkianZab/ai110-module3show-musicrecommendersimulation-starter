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

Real-world platforms like Spotify combine two approaches: collaborative filtering, which
recommends based on patterns across many users' listening behavior ("people who liked
this also liked..."), and content-based filtering, which recommends based on a song's own
attributes matched against a listener's known preferences. This simulation implements
only the content-based half, at a small scale.

Each `Song` carries: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`,
and `acousticness`. Each `UserProfile` stores a narrower set of preferences: `favorite_genre`,
`favorite_mood`, `target_energy`, and `likes_acoustic`. The profile doesn't track every
song attribute — tempo, valence, and danceability have no matching preference field, which
means the `Recommender` either ignores them or treats them as secondary signals.

The `Recommender` scores each song by comparing it against the user's profile:
- **Genre match**: full points if `song.genre == user.favorite_genre`, otherwise none.
- **Mood match**: full points if `song.mood == user.favorite_mood`, otherwise none.
- **Energy closeness**: partial credit based on how close `song.energy` is to
  `user.target_energy`, rather than rewarding high or low energy outright — a song 
  isn't penalized for being energetic if the user wants energy, or calm if they don't.
- **Acoustic preference**: if `user.likes_acoustic` is True, songs with higher
  `acousticness` score better; if False, the opposite.

Genre is weighted most heavily since it's the strongest single predictor of whether a
song fits someone's overall taste. Mood is weighted second, since it captures emotional
tone that genre alone can miss. Energy and acousticness contribute smaller, secondary
weights since they refine the match rather than define it.

To choose which songs to recommend, every song in the catalog is scored, then sorted
from highest to lowest score. The top `k` songs are returned as the final recommendations.
This separation matters: the *scoring rule* only knows how to grade one song against one
profile — it has no sense of how that song compares to the rest of the catalog. The
*ranking rule* takes all those scores and decides the actual order the user sees, and
would also be the place to add things like tie-breaking or diversity constraints.

### Data Flow

​```mermaid
flowchart LR
    A[User Prefs dict] --> C{For each song in CSV}
    B[songs.csv → list of dicts] --> C
    C --> D[score_song: genre +3, mood +2, energy ≤1.5, acoustic ≤1.0]
    D --> E[List of song, score, reasons]
    E --> F[Sort descending by score]
    F --> G[Top k → print title, score, explanation]
​```

### Algorithm Recipe

- **+3.0** — genre exact match
- **+2.0** — mood exact match
- **up to +1.5** — energy closeness: `1.5 × (1 − |song.energy − target_energy|)`
- **up to +1.0** — acoustic fit: `acousticness` if the user likes acoustic, `1 − acousticness` if not
- Maximum possible score: 7.5

### Expected Biases

Because genre carries the largest weight and requires an exact string match, the system
will over-prioritize genre: "indie pop" scores zero genre points against a "pop" preference
even though the genres are closely related. It also has no way to express dislike — a song
from a genre the user hates and a song from a neutral genre are treated identically. Finally,
every song a user hasn't matched on genre or mood competes only on energy and acousticness,
which compresses most of the catalog into a narrow score band.

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

## Sample Recommendation Output

```
User profile: genre=pop, mood=happy, energy=0.8, likes_acoustic=False

Loaded songs: 18

Top recommendations:

1. Sunrise City — Neon Echo  [score: 7.29]
   why: genre match (+3.0); mood match (+2.0); energy closeness (+1.47); acoustic fit (+0.82)

2. Gym Hero — Max Pulse  [score: 5.25]
   why: genre match (+3.0); energy closeness (+1.30); acoustic fit (+0.95)

3. Rooftop Lights — Indigo Parade  [score: 4.09]
   why: mood match (+2.0); energy closeness (+1.44); acoustic fit (+0.65)

4. Bassline Eruption — DJ Kavo  [score: 2.25]
   why: energy closeness (+1.28); acoustic fit (+0.97)

5. Concrete Poetry — MC Verse  [score: 2.24]
   why: energy closeness (+1.36); acoustic fit (+0.88)
```

---

## Experiments You Tried

**Weight shift: genre 3.0 → 1.5, energy 1.5 → 3.0.** I halved the genre weight and doubled
the energy weight, expecting the rankings to flip toward pure energy matching. Surprisingly,
the #1 results didn't change: Sunrise City still won High-Energy Pop (7.08 vs the old 7.20)
and Storm Runner still won Deep Intense Rock. Songs that match both genre AND mood are so
far ahead that they survive even a major reweighting — the top of the ranking is robust.

What changed was everything below #1. The score gaps compressed dramatically: unmatched
high-energy songs like Bassline Eruption jumped from 2.40 to ~3.82, nearly catching
Rooftop Lights (a genuine mood match) at ~5.23. The bottom of every top-5 filled with
interchangeable high-energy tracks regardless of genre or mood. My conclusion: the change
made the recommendations *different*, not more accurate — energy is too crude a signal to
lead, because two songs with identical energy can feel completely unrelated. I reverted
to the original weights.

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



