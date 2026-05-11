# Art Crime Ledger

A Python and SQLite simulation of a fictional art crime ring operating in present-day Paris. The project is the books — the operational records of a nine-person crew that targets museums, forges replacements, and moves art through the underground market. Built to learn data engineering by building a world.

## The World

Paris, present day. The crew is nine: a former curator turned mastermind, a Dutch security specialist who cracks museum vaults, a getaway driver out of Marseille, a Swedish art critic with a real byline and a real second life, and others. They target the Louvre, the Orsay, the Marmottan, the Pompidou. Some jobs go clean. Some don't.

The data is fictional but the museums and artworks are real.

## Tech

- Python 3
- SQLite (built in, no installation needed)
- No external dependencies yet

## Running It

Clone the repo, then from inside the project folder:

```bash
python setup.py        # creates the database and four tables
python seed_crew.py    # inserts the nine crew members
python expand_marks.py # inserts 24 real Paris artworks with auto-calculated difficulty
```

Then to read the data back:

```bash
python list_crew.py    # lists crew, sorted by skill
python list_marks.py   # lists marks, sorted by difficulty
python list_jobs.py    # lists all recorded jobs with crew and payouts
```

The database lives in `ledger.db`. It's gitignored — you build it fresh from the scripts.

## Files

- `setup.py` — schema definitions for the `crew`, `marks`, `jobs`, and `job_crew` tables
- `seed_crew.py` — populates the crew table with nine members
- `expand_marks.py` — populates the marks table with 24 real Paris artworks; auto-calculates security difficulty based on museum tier and estimated value
- `list_crew.py` — reads and displays the crew, sorted by skill
- `list_marks.py` — reads and displays all marks, sorted by difficulty
- `list_jobs.py` — reads and displays all recorded jobs with crew payouts, using JOIN queries across four tables

## Status

Four tables: `crew`, `marks`, `jobs`, `job_crew`. Nine crew members, 24 marks across five Paris museums and two private galleries. No jobs on the books yet — the simulator is next.

Coming next: `simulator.py` — a function that picks a mark, assembles a crew, rolls the outcome based on skill vs difficulty, and writes the result to the database. Run it once and generate a full year of heists.