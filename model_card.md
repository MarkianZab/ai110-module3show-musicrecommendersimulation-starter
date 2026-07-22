# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0** — a small content-based music recommender that scores songs by how
closely they match a user's stated taste.

## 2. Intended Use

VibeMatch generates a ranked top-5 list of songs from a fixed 18-song catalog based on a
user's favorite genre, favorite mood, energy level, and whether they like acoustic sound.
It assumes the user can accurately describe their own taste in those four fields, and that
their preferences fit categories that exist in the catalog.

This is a classroom simulation built to learn how recommenders work — it is not meant for
real users. It should not be used to make claims about anyone's actual musical taste, and
it has no way to handle users whose preferences fall outside its tiny catalog (it will
confidently recommend songs anyway, which is one of its documented weaknesses).

## 3. How the Model Works

Every song gets graded against the user's profile like a scorecard. If the song's genre
matches the user's favorite genre, it earns 3 points — the biggest single reward, because
genre is usually the strongest signal of whether someone will like a song. A mood match
earns 2 points. Then energy is scored by closeness, not size: a song isn't rewarded for
being more energetic, it's rewarded for being *near* the energy level the user asked for,
earning up to 1.5 points that shrink as the gap grows. Finally, up to 1 point comes from
acoustic fit — acoustic-sounding songs score higher for users who like acoustic, and
lower for users who don't. The maximum possible score is 7.5.

Once every song in the catalog has a score, the list is sorted from highest to lowest and
the top 5 are shown, each with a plain-English explanation of exactly where its points
came from.

The starter code came with empty function stubs, so all of the scoring logic above was
designed and added from scratch, along with an expanded catalog (10 songs to 18) covering
8 new genres and moods.

## 4. Data

The catalog holds 18 songs, each described by genre, mood, energy, tempo, valence,
danceability, and acousticness. It covers 15 genres (pop, lofi, rock, ambient, jazz,
synthwave, indie pop, hip-hop, classical, folk, edm, r&b, metal, latin, indie rock) and
14 moods. I expanded it from the original 10 songs to add diversity.

Limits: 18 songs is tiny — most genres have exactly one song, so "recommending within a
genre" barely means anything. Whole dimensions of musical taste are missing entirely:
lyrics, language, artist popularity, era, and how songs actually sound. The catalog also
skews toward chill acoustic music, which quietly shapes what unmatched users get recommended.

## 5. Strengths

The system works well for users whose taste lines up with the catalog. The Chill Lofi
profile got exactly the right top 3, and the explanations make every ranking auditable —
you can always see why a song scored what it did. The best result was Spacewalk Thoughts:
an ambient song that ranked 4th for the lofi user because its chill mood and acoustic
sound carried it across the genre boundary. That's the system correctly finding "same
vibe, different label," which is the whole point of content-based filtering. The
closeness-based energy scoring also behaves correctly at both extremes — calm songs win
for low-energy users and intense songs win for high-energy users, rather than high energy
always being treated as better.

## 6. Limitations and Bias

The biggest weakness I found is how the system behaves when a user's taste isn't in the
catalog at all. I tested a profile asking for angry country music — a genre and mood that
don't exist in my dataset. Instead of signaling that it couldn't find a good match, the
system confidently returned a top 5 where the scores were nearly identical (2.09 to 2.19,
a spread of just 0.10 points). The "ranking" at that point is basically noise. Worse,
four of the five recommendations were chill lofi-style songs, because acoustic low-energy
tracks happen to dominate my catalog — so a user asking for angry country gets served
study music, with no warning that the system is guessing. This is a small-scale version
of the cold-start problem real recommenders face with new users.

## 7. Evaluation

I tested five user profiles: three normal ones (High-Energy Pop, Chill Lofi, Deep Intense
Rock) and two adversarial ones designed to stress the scoring logic — a "conflicted" user
with a sad mood but very high energy, and a "no matches" user whose genre and mood don't
exist in the catalog. For each profile I looked at whether the top 5 made intuitive sense,
how large the score gaps were, and whether the explanations matched why I'd expect each
song to rank where it did.

### Test Outputs

**High-Energy Pop** — `{genre: pop, mood: happy, energy: 0.9, likes_acoustic: False}`

```
1. Sunrise City — Neon Echo  [score: 7.20]
   why: genre match (+3.0); mood match (+2.0); energy closeness (+1.38); acoustic fit (+0.82)
2. Gym Hero — Max Pulse  [score: 5.41]
   why: genre match (+3.0); energy closeness (+1.46); acoustic fit (+0.95)
3. Rooftop Lights — Indigo Parade  [score: 3.94]
   why: mood match (+2.0); energy closeness (+1.29); acoustic fit (+0.65)
4. Bassline Eruption — DJ Kavo  [score: 2.40]
   why: energy closeness (+1.43); acoustic fit (+0.97)
5. Storm Runner — Voltline  [score: 2.38]
   why: energy closeness (+1.48); acoustic fit (+0.90)
```

**Chill Lofi** — `{genre: lofi, mood: chill, energy: 0.35, likes_acoustic: True}`

```
1. Library Rain — Paper Lanterns  [score: 7.36]
   why: genre match (+3.0); mood match (+2.0); energy closeness (+1.50); acoustic fit (+0.86)
2. Midnight Coding — LoRoom  [score: 7.10]
   why: genre match (+3.0); mood match (+2.0); energy closeness (+1.40); acoustic fit (+0.71)
3. Focus Flow — LoRoom  [score: 5.21]
   why: genre match (+3.0); energy closeness (+1.42); acoustic fit (+0.78)
4. Spacewalk Thoughts — Orbit Bloom  [score: 4.32]
   why: mood match (+2.0); energy closeness (+1.40); acoustic fit (+0.92)
5. Coffee Shop Stories — Slow Stereo  [score: 2.36]
   why: energy closeness (+1.47); acoustic fit (+0.89)
```

**Deep Intense Rock** — `{genre: rock, mood: intense, energy: 0.95, likes_acoustic: False}`

```
1. Storm Runner — Voltline  [score: 7.34]
   why: genre match (+3.0); mood match (+2.0); energy closeness (+1.44); acoustic fit (+0.90)
2. Gym Hero — Max Pulse  [score: 4.42]
   why: mood match (+2.0); energy closeness (+1.47); acoustic fit (+0.95)
3. Bassline Eruption — DJ Kavo  [score: 2.47]
   why: energy closeness (+1.50); acoustic fit (+0.97)
4. Iron Choir — Blackpine  [score: 2.41]
   why: energy closeness (+1.47); acoustic fit (+0.94)
5. Sunrise City — Neon Echo  [score: 2.12]
   why: energy closeness (+1.30); acoustic fit (+0.82)
```

**Conflicted: sad but hyped** — `{genre: edm, mood: sad, energy: 0.95, likes_acoustic: False}`

```
1. Bassline Eruption — DJ Kavo  [score: 5.47]
   why: genre match (+3.0); energy closeness (+1.50); acoustic fit (+0.97)
2. Empty Platform — Grey Season  [score: 3.10]
   why: mood match (+2.0); energy closeness (+0.73); acoustic fit (+0.37)
3. Gym Hero — Max Pulse  [score: 2.42]
   why: energy closeness (+1.47); acoustic fit (+0.95)
4. Iron Choir — Blackpine  [score: 2.41]
   why: energy closeness (+1.47); acoustic fit (+0.94)
5. Storm Runner — Voltline  [score: 2.34]
   why: energy closeness (+1.44); acoustic fit (+0.90)
```

**No matches anywhere** — `{genre: country, mood: angry, energy: 0.5, likes_acoustic: True}`

```
1. Coffee Shop Stories — Slow Stereo  [score: 2.19]
   why: energy closeness (+1.30); acoustic fit (+0.89)
2. Library Rain — Paper Lanterns  [score: 2.13]
   why: energy closeness (+1.27); acoustic fit (+0.86)
3. Focus Flow — LoRoom  [score: 2.13]
   why: energy closeness (+1.35); acoustic fit (+0.78)
4. Dust Road Home — Wren Hollow  [score: 2.12]
   why: energy closeness (+1.25); acoustic fit (+0.88)
5. Midnight Coding — LoRoom  [score: 2.09]
   why: energy closeness (+1.38); acoustic fit (+0.71)
```

### What I compared and what surprised me

**High-Energy Pop vs. Chill Lofi:** The two top-5 lists share zero songs, which is what
should happen — these profiles sit at opposite ends of energy and acousticness. This
confirmed the profile fields actually drive real differentiation. The nicest surprise was
in the Chill Lofi results: Spacewalk Thoughts, an ambient song, beat out jazz and other
options despite not matching the lofi genre, because its chill mood and high acousticness
carried it. The system found a song with the right vibe across a genre boundary — exactly
what a content-based recommender is supposed to do.

**Deep Intense Rock vs. Conflicted (sad + high energy):** These two profiles have opposite
moods, but their results share four of the same five songs. When the mood preference fails
to find matches, energy quietly takes over the ranking. The conflicted profile exposed a
hidden priority in my weights: the user said they felt sad, but the #1 result was Bassline
Eruption — a euphoric EDM track — at 5.47, while Empty Platform, the only actually sad song,
came second at 3.10. My +3 genre weight silently outvoted the user's stated mood. The system
never resolves the conflict; it just lets the bigger number win, and nothing in the output
tells the user that happened.

**Normal profiles vs. the no-match profile:** For real profiles, the #1 song wins by a
large margin (7.20 vs 5.41 for pop; 7.34 vs 4.42 for rock) — the ranking is confident and
meaningful. For the no-match profile, all five scores landed between 2.09 and 2.19, a
spread of just 0.10 points. The ranking still *looks* authoritative but is essentially
noise, and it defaulted to serving chill acoustic songs to a user who asked for angry
country — because that's simply what my catalog has the most of.

**Why does Gym Hero keep showing up?** In plain terms: Gym Hero is a pop song with very
high energy, so it collects the big genre bonus from any pop-loving user AND nearly full
energy points from any high-energy user. It only ever loses the mood points. Since just
one song in the whole catalog (Sunrise City) matches pop AND happy, Gym Hero is permanently
the runner-up — a song labeled "intense" that keeps being recommended to people who asked
for happy music.

## 8. Future Work

1. **Genre similarity instead of exact matching.** "Indie pop" should earn partial credit
   against a "pop" preference instead of zero. A small similarity table between related
   genres would fix the sharpest filter bubble.
2. **A confidence signal.** When all top-5 scores land within a 0.1-point spread (like my
   no-match test), the system should say "weak matches" instead of presenting noise as a
   confident ranking.
3. **Dislikes.** Let users mark genres or moods to avoid, with negative points — right now
   a hated genre and a neutral genre are treated identically.

## 9. Personal Reflection

My biggest learning moment was the energy scoring. My first instinct was "user wants
energy, so higher energy should score higher" — and seeing why that's broken (a chill
user would get gym music) taught me the difference between rewarding a value and
rewarding *closeness to a target*. One line of math, `1 - abs(song - target)`, but the
idea behind it changed how I think about matching problems in general.

AI tools accelerated everything — drafting code, generating catalog data, explaining
`.sort()` vs `sorted()` — but the project only worked because I verified the outputs
myself. When the recommender ran, I checked the scores by hand against the formula
(Sunrise City: 3 + 2 + 1.47 + 0.82 = 7.29) before trusting the rankings. The AI also
made predictions about my experiment results that I had to actually run the code to
confirm. The pattern I'll keep: let AI draft, but own the verification.

What surprised me most is how little it takes to *feel* like a real recommender. Two
if-statements and two distance formulas produced rankings that mostly matched my
intuition — and the failure cases were interesting rather than random. A user asking
for "sad but hyped" music got euphoric EDM because my genre weight silently outvoted
their mood, and a user with no matches got confidently served study music. Real
recommenders are enormously more complex, but the core dynamic — weights encoding
hidden priorities the user never sees — is clearly the same.

If I extended this, I'd start with genre similarity scoring, then try a simple
collaborative layer: simulate a few users with listening histories and recommend based
on overlap, so I could compare both approaches on the same catalog.