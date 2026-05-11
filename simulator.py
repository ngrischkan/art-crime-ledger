import sqlite3
import random
from datetime import date, timedelta

def run_job(cursor, mark_id, crew_ids):
    # Step 1: look up the mark
    cursor.execute("SELECT estimated_value, security_difficulty FROM marks WHERE id = ?", (mark_id,))
    mark = cursor.fetchone()
    mark_value, mark_difficulty = mark

    # Step 2: look up crew skills using IN clause
    placeholders = ",".join("?" * len(crew_ids))
    cursor.execute(f"SELECT skill FROM crew WHERE id IN ({placeholders})", crew_ids)
    skill_rows = cursor.fetchall()

    # Step 3: calculate average skill
    avg_skill = sum(row[0] for row in skill_rows) / len(skill_rows)

    # Step 4: calculate success chance
    skill_advantage = avg_skill - mark_difficulty
    success_chance = 0.5 + (skill_advantage * 0.08)
    success_chance = max(0.15, min(0.95, success_chance))

    # Step 5: roll outcome
    roll = random.random()
    if roll < success_chance:
        outcome = "clean"
        gross_take = mark_value * random.uniform(0.85, 1.0)
    elif roll < success_chance + 0.15:
        outcome = "partial"
        gross_take = mark_value * random.uniform(0.3, 0.6)
    else:
        outcome = "botched"
        gross_take = 0.0

    # Step 6: calculate expenses
    expenses = gross_take * random.uniform(0.02, 0.06)

    # Step 7: generate a random date between 2023-01-01 and 2024-12-31
    start = date(2023, 1, 1)
    end = date(2024, 12, 31)
    job_date = (start + timedelta(days=random.randint(0, (end - start).days))).isoformat()

    # Step 8: insert job row, capture lastrowid
    cursor.execute("""
        INSERT INTO jobs (mark_id, date, outcome, gross_take, expenses, net_profit, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (mark_id, job_date, outcome, gross_take, expenses, 0.0, f"Simulated job — outcome: {outcome}"))
    job_id = cursor.lastrowid

    # Step 9: insert job_crew rows
    total_payouts = 0.0
    for crew_id in crew_ids:
        cursor.execute("SELECT cut_percentage FROM crew WHERE id = ?", (crew_id,))
        cut = cursor.fetchone()[0]
        payout = gross_take * cut
        total_payouts += payout
        cursor.execute("""
            INSERT INTO job_crew (job_id, crew_id, role_on_job, payout)
            VALUES (?, ?, ?, ?)
        """, (job_id, crew_id, "crew", payout))

    # Step 10: update net_profit
    net_profit = gross_take - expenses - total_payouts
    cursor.execute("UPDATE jobs SET net_profit = ? WHERE id = ?", (net_profit, job_id))

    # Step 11: return outcome
    return outcome


def simulate_year(cursor, num_jobs=50):
    cursor.execute("SELECT id FROM marks")
    all_mark_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM crew")
    all_crew_ids = [row[0] for row in cursor.fetchall()]

    results = {"clean": 0, "partial": 0, "botched": 0}

    for i in range(num_jobs):
        mark_id = random.choice(all_mark_ids)
        crew_size = random.randint(4, 6)
        crew_ids = random.sample(all_crew_ids, crew_size)
        outcome = run_job(cursor, mark_id, crew_ids)
        results[outcome] += 1
        print(f"Job {i+1:>3}: mark_id={mark_id} crew={crew_ids} → {outcome}")

    print(f"\nResults: {results}")


if __name__ == "__main__":
    conn = sqlite3.connect("ledger.db")
    cursor = conn.cursor()
    simulate_year(cursor, num_jobs=50)
    conn.commit()
    conn.close()
    print("Done. 50 jobs recorded.")