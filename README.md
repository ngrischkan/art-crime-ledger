# Art Crime Ledger

A Python and SQLite simulation of a fictional art crime ring operating in present-day Paris. The project is the books — the operational records of a nine-person crew that targets museums, forges replacements, and moves art through the underground market. Built to learn data engineering by building a world.

**Live dashboard:** https://grischkan-art-crime-ledger.streamlit.app

## The World

Paris, present day. The crew is nine: a former curator turned mastermind, a Dutch security specialist who cracks museum vaults, a getaway driver out of Marseille, a Swedish art critic with a real byline and a real second life, and others. They target the Louvre, the Orsay, the Marmottan, the Pompidou. Some jobs go clean. Some don't.

The data is fictional but the museums and artworks are real.

## Tech

- Python 3
- SQLite (built in, no installation needed)
- Streamlit + Plotly (for the dashboard — `pip install -r requirements.txt`)

## Running It

Clone the repo, then from inside the project folder:

```bash
python setup.py        # creates the database and four tables
python seed_crew.py    # inserts the nine crew members
python expand_marks.py # inserts 24 real Paris artworks with auto-calculated difficulty
python simulator.py    # generates 50 jobs with randomized outcomes and updates crew heat
```

Then to read the data back:

```bash
python list_crew.py    # lists crew, sorted by skill
python list_marks.py   # lists marks, sorted by difficulty
python list_jobs.py    # lists all recorded jobs with crew and payouts
python analysis.py     # prints earnings, target frequency, and museum success rates
```

To run the dashboard:

```bash
python -m streamlit run dashboard.py
```

To cool down the crew over time:

```bash
python decay_heat.py   # reduces every crew member's heat by 1 (min 0)
```

The database lives in `ledger.db`. It's included in the repo — clone and run the dashboard directly.

## Files

- `setup.py` — schema definitions for the `crew`, `marks`, `jobs`, and `job_crew` tables
- `seed_crew.py` — populates the crew table with nine members
- `expand_marks.py` — populates the marks table with 24 real Paris artworks; auto-calculates security difficulty based on museum tier and estimated value
- `simulator.py` — picks a random mark, assembles a 4–6 person crew, rolls outcome based on skill vs difficulty, writes the job to the database, and updates crew heat
- `decay_heat.py` — reduces every crew member's heat by 1 (min 0); run it to simulate time passing between jobs
- `list_crew.py` — reads and displays the crew, sorted by skill
- `list_marks.py` — reads and displays all marks, sorted by difficulty
- `list_jobs.py` — reads and displays all recorded jobs with crew payouts, using JOIN queries across four tables
- `analysis.py` — three summary queries: total earnings per crew member, most-targeted artworks, clean job success rate by museum
- `dashboard.py` — Streamlit dashboard visualizing the analysis queries as charts and tables

## Heat System

Every crew member carries a heat value. After a clean job, each participant gains 1 heat. After a botched job, each participant gains 3. Partial jobs carry no heat. Run `decay_heat.py` to tick heat down by 1 across the board — simulating time passing and attention fading.

## Status

Four tables: `crew`, `marks`, `jobs`, `job_crew`. Nine crew members, 24 marks across five Paris museums and two private galleries. 50 simulated jobs on the books. Streamlit dashboard live.
