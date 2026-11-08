# Did the satellite see the Lagos flood? Radar evidence from Lekki, 30 June 2026

*Project report, version 1 (7 November 2026). Written in plain English; technical terms are explained where they first appear. A draft that can be adapted for Medium.*

## The question
Heavy rain flooded parts of Lagos at the end of June 2026. News outlets named Lekki and Victoria Island, and a Lagos State commissioner called the rainfall of Tuesday 30 June an extreme event. I was staying at Orchid, Lekki, that week and saw the flooding myself.

People who respond to floods, plan cities or assess damage need more than "it flooded". They need to know where the ground changed, how sure we can be, and whether someone else can check the work. Satellites pass over Lagos every few days, whatever the weather. This project asks: **did a satellite record the Lekki flood, and can that record be turned into honest, repeatable evidence?**

## The data
- **Sentinel-1 radar** (European Space Agency, free). Radar sends its own microwave pulse and listens for the echo (*backscatter*, measured in decibels, dB), so it sees through cloud and works at night. Sentinel-1D passed over Lekki at **06:29 on 30 June 2026**, the flood morning.
- **Comparison pictures:** the same satellite on the same path in August 2026 (a normal month), plus control days (below).
- **Rainfall:** NASA's satellite rain estimate (GPM IMERG). It shows 48 mm fell over the area in the 48 hours before the flood-morning pass.
- **Where water normally is:** the JRC Global Surface Water map (1984–2021).
- **Place names:** news reports, positioned with OpenStreetMap.

All processing ran in Google Earth Engine's free noncommercial tier. **Total cost: $0.**

## What I did, step by step
1. **Checked that the satellite actually saw the event** (milestone 1). Found the 30 June pass, checked its timing against dated news reports and exported a first sample.
2. **Made the processing repeatable** (milestone 2). One command takes a small settings file (place, dates, satellite) and produces two aligned pictures plus a *receipt*: the picture IDs, software versions, file fingerprints and Earth Engine's step-by-step recipe. Five runs on two computers, and later a fresh install from GitHub, gave **byte-identical** files.
3. **Read the pictures honestly** (milestone 3), on a 5 km square of central Lekki:
   - **Smoothing:** radar pictures are grainy (*speckle*). Each pixel was averaged with its 5 × 5 neighbours (50 m), in real power units, not dB.
   - **Control days:** to tell a flood from ordinary noise and ordinary rain, the same comparison was run for **10 September** (as rainy as flood day: 49 mm) and **22 September** (dry).
   - **Practice and test halves:** the two rule numbers were chosen on the west half only, locked in a commit, then applied once to the unseen east half, like setting an exam before seeing the answers.
   - **Labels:** every pixel got one label: *land got louder*, *always water*, *new dark water*, *can't tell*, *no change* or *not observed*.
4. **Tested how sure we can be** (milestone 4): nine different rule settings, a second "normal" period (January 2026, from the twin satellite Sentinel-1A), the next heavy rain (12 July), and checks at named places.
5. **Published the results in a standard format** (milestone 5): a STAC catalogue, the "library cards" of the satellite world, validated against the official schemas and searchable through a local STAC API.
6. **Built a clickable map** (milestone 6) and **release checks** (milestone 7).

## What we found
**1. The flood morning stands out clearly from normal days.**

| Comparison with August (test half, unseen by the rules) | Land that got much louder |
|---|---|
| **30 June, flood morning** | **9.4%** (about 1.1 km²) |
| 10 September, equally rainy, no reported flood | 0.7% |
| 22 September, dry | 0.8% |

**2. The signal is brightening, not darkening.** Calm open water normally looks *dark* to radar, but almost no new dark water appeared (under 0.01%). In a city, water in a street bounces the pulse off building walls and back to the satellite (*double bounce*), so flooded streets can look *brighter*. The result fits that.

**3. It survives the obvious objections.**
- *"It's just grain."* No: smoothing brought the control days below 1% while the flood day kept about 10%.
- *"It's just rain."* No: an equally rainy day showed about one-twelfth as much.
- *"You tuned the rules to fit."* No: the rules were set on the west half and held on the east half.
- *"August was a strange month."* No: against a January dry-season baseline, flood day was 17% and a dry day 2.4%, and 81% of the brightened spots matched.
- *"Different rule numbers would change everything."* The size of the area depends on the rules (5%–17%), but under all nine settings the flood day was 6 to 15 times the control days.

**4. The same spots light up again.** On 12 July, after even heavier rain (84 mm), 43% of the flood-morning bright spots on the test half lit up again (chance would give about 9%), while almost none did on normal days. That is consistent with flood-prone streets.

## What we cannot say
- **This is not a flood map.** No source gives the water's edge at 06:29, so no accuracy figures (such as precision or recall) can honestly be calculated, and none are claimed.
- **It does not identify individual flooded streets.** At five places named in the news, flood day was higher than both control days, but only two were above the area's average.
- **Brightening has other causes**, such as construction or parked vehicles. Control days reduce these but cannot rule them out.
- **50 m smoothing can erase narrow flooded streets.**
- **One satellite pass**, at 06:29. The rain continued until about 14:00.

**The defensible claim:** *on the morning of 30 June 2026, about 10% of land in a 5 km area of central Lekki (range 5–17% depending on reasonable rule choices) showed radar brightening 6–15 times the rate of equally rainy and dry days processed the same way. That is measured surface change consistent with the reported urban flooding, not a validated flood-extent map.*

## Mistakes and what they taught
- An early search for May returned nothing and drew a broken map. The code now stops loudly on empty searches.
- A receipt once named a code version that did not contain the code that actually ran. Receipts now flag unsaved code.
- I typed an impossible date (31 June). Earth Engine refused it, and the settings check now catches it before going online.
- The textbook "dark = water" rule failed in Lekki. Rather than force it, the project reports brightening and states the limits.

## Who did what
I chose the case, supplied the first-hand flood account, created the accounts, ran the first seven Earth Engine scripts in the Code Editor, exported the first sample, and made the scope decisions: widening to 5 km, growing the area in steps, and the persistence check, which was my idea. **The Python code, analyses and write-ups were produced with an AI assistant (Claude, Anthropic)**, working with me in guided sessions. I directed the work and reviewed each step. The assistant wrote and ran the code. Every number in this report comes from files in the repository.

## Reproduce it
See the README. In short: Python 3.13, `pip install -r requirements.txt`, a free Earth Engine noncommercial project, then the commands listed there. Every result above has a script, a receipt and an evidence file (`evidence/`, `evaluation/ASSESSMENT.md`).

## Next steps (planned, not done)
- Extend to the Lekki–Victoria Island corridor, which covers all the news-named places.
- Look for located, timed flood photos to allow a real accuracy check.
- Try a second city (Port Harcourt).

*Contains modified Copernicus Sentinel data (2026), processed in Google Earth Engine. JRC Global Surface Water © EC JRC/Google. Place positions © OpenStreetMap contributors.*
