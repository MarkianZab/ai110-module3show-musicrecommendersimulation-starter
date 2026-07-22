# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

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

---

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
