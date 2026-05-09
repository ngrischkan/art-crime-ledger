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
python setup.py              # creates the database and tables
python seed_crew.py          # inserts the nine crew members
python seed_marks.py         # inserts the starting set of art targets
python record_first_job.py   # records the first historical heist
```

Then to read the data back:

```bash
python list_crew.py          # lists crew, sorted by skill
python list_marks.py         # lists marks, sorted by difficulty
```

The database lives in `ledger.db`. It's gitignored — you build it fresh from the scripts.

## Files

- `setup.py` — schema definitions for the `crew`, `marks`, `jobs`, and `job_crew` tables
- `seed_crew.py` — populates the crew table
- `seed_marks.py` — populates the marks table
- `list_crew.py` — reads and displays the crew
- `list_marks.py` — reads and displays the marks
- `record_first_job.py` — records the crew's first historical heist (a Rodin sculpture lifted in August 2023)

## Status

Four tables: `crew`, `marks`, `jobs`, `job_crew`. The crew exists, the targets exist, and the books now record one historical job — a Rodin sculpture lifted in August 2023.

Coming next: a simulator that runs jobs procedurally, and JOIN-based analysis queries for spotting patterns across multiple jobs.