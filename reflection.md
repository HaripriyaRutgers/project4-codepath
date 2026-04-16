# Reflection: Comparing User Profile Pairs

---

## Pair 1: Happy Pop Fan vs. Low-Energy Pop Fan

**Profile A:** genre = pop, energy = 0.8  
**Profile B:** genre = pop, energy = 0.15

Both profiles want pop music. The only difference is how energetic they want it to be.

Profile A gets exactly what you would expect — "Sunrise City" comes first, "Gym Hero" comes second. Both are pop songs with high energy, so the system is working correctly here.

Profile B is where things get strange. You might expect pop songs to still dominate since the genre preference is the same. But the catalog's pop songs are all high-energy (0.82 and 0.93), so they are far from the 0.15 target. The energy penalty is so large that "Golden Hour," a classical piano piece, scores higher than any pop song. A user who typed in "pop" as their favorite genre gets a classical recommendation at the top of their list — with no explanation of why.

**Why it makes sense (and why it is also a problem):** The system is doing the math correctly — the classical song really is closer to 0.15 energy than any pop song. But the user did not ask for classical music. The scoring treats energy and genre as independent levers and adds them together, so a big enough energy advantage can always overpower a genre preference.

---

## Pair 2: EDM Fan vs. Folk and Acoustic Fan

**Profile A:** genre = edm, energy = 0.95  
**Profile B:** genre = folk, energy = 0.25

These two profiles sit at opposite ends of the energy spectrum, and the results reflect that clearly.

The EDM fan gets "Electric Pulse" at the top with a near-perfect score because the one EDM song in the catalog happens to be at exactly the right energy level. Everything lines up. After that first result, the next songs drop significantly in score and are all high-energy tracks from metal, pop, and rock — no other EDM songs exist in the catalog to fill the list.

The folk fan gets "Mountain Whisper" at the top, which is the right genre and close to the right energy. However, the second result is "Starlit Dreams," a new age song, because it happens to sit at exactly 0.25 energy and earns a perfect energy score. No folk, no acoustic guitar — just the right number.

**Why it makes sense:** EDM profile prefers high-energy songs, so the whole top five shifts toward loud, driving tracks. The folk and acoustic profile shifts toward quiet, slow tracks. The energy preference is doing most of the work for both users. The genre match is a bonus when it happens, but the system is really sorting by proximity to the energy target first.

---

## Pair 3: High-Energy Lofi Fan vs. Calm Metal Fan

**Profile A:** genre = lofi, energy = 0.90  
**Profile B:** genre = metal, energy = 0.20

These are the two "conflicting" profiles — the genre and energy preferences point in opposite directions for both users.

The high-energy lofi fan still gets lofi songs at the top because the genre bonus (+3.0) is enough to keep them ahead of non-lofi songs, even with an energy penalty. "Midnight Coding" scores 5.6 while the nearest high-energy non-lofi song scores only 4.9. So the genre preference survives — barely.

The calm metal fan has a worse experience. There is only one metal song in the catalog ("Firestorm," energy = 0.97), and it sits as far as possible from the 0.20 energy target. It scores 4.15. Three songs from completely unrelated genres — classical, new age, and folk — all score higher. The metal fan ends up with a top five that contains zero metal songs past the first position, and even that first position only scrapes in at number four.

**Why it makes sense (and why it is a problem):** When a genre has only one song and that song's energy is far from what the user wants, the genre becomes useless as a signal. The lofi fan survives because lofi has three songs at varied energies, giving the genre bonus more chances to apply. The metal fan is stuck because the catalog does not support their combination of preferences. This is not the user's fault — it is a gap in the data.

---

## On "Gym Hero" Showing Up for Happy Pop Fans

This one is worth explaining separately because it comes up every time the default profile runs.

"Gym Hero" is a pop song about working out. Its mood is "intense," not "happy." So why does it keep appearing in results for someone who asked for happy pop music?

With the mood check currently turned off, the recommender only looks at genre and energy. "Gym Hero" is tagged as pop (genre match, +3.0 points) and has an energy of 0.93, which is close to the 0.8 target (energy score of 4.35 points). That adds up to 7.35 — the second-highest score of any song in the catalog for this profile.

The system is not wrong by its own rules. It found a pop song with energy close to what was requested and rewarded it. The problem is that the user asked for "happy" music and got a workout track instead, and the system has no way to tell the difference right now because the mood signal is disabled. When the mood check is turned back on, "Gym Hero" would drop by 2.0 points (no mood match) and fall further down the list, which is the more correct behavior.

This illustrates the core tradeoff in the current design: the fewer signals you use, the more the remaining ones get stretched to cover cases they were not meant to handle.
