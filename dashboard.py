import sqlite3
import streamlit as st

st.set_page_config(page_title="Art Crime Ledger", layout="wide")
st.title("Art Crime Ledger — Operations Dashboard")

conn = sqlite3.connect("ledger.db")

# --- Crew earnings ---
st.header("Crew Earnings")

rows = conn.execute("""
    SELECT c.nickname, SUM(jc.payout) as total_earned
    FROM job_crew jc
    JOIN crew c ON jc.crew_id = c.id
    GROUP BY c.nickname
    ORDER BY total_earned DESC
""").fetchall()

nicknames = [r[0] for r in rows]
earnings = [r[1] for r in rows]

st.bar_chart({"Total Earned ($)": dict(zip(nicknames, earnings))})

# --- Most targeted artworks ---
st.header("Most Targeted Artworks")

rows = conn.execute("""
    SELECT m.title, COUNT(*) as times_targeted
    FROM jobs j
    JOIN marks m ON j.mark_id = m.id
    GROUP BY m.title
    ORDER BY times_targeted DESC
""").fetchall()

titles = [r[0] for r in rows]
counts = [r[1] for r in rows]

st.bar_chart({"Times Targeted": dict(zip(titles, counts))})

# --- Museum success rates ---
st.header("Success Rate by Museum")

rows = conn.execute("""
    SELECT m.location,
           COUNT(*) as total_jobs,
           SUM(CASE WHEN j.outcome = 'clean' THEN 1 ELSE 0 END) as clean_jobs,
           ROUND(100.0 * SUM(CASE WHEN j.outcome = 'clean' THEN 1 ELSE 0 END) / COUNT(*), 1) as success_rate
    FROM jobs j
    JOIN marks m ON j.mark_id = m.id
    GROUP BY m.location
    ORDER BY success_rate DESC
""").fetchall()

col1, col2 = st.columns([1, 1])

with col1:
    locations = [r[0] for r in rows]
    rates = [r[3] for r in rows]
    st.bar_chart({"Success Rate (%)": dict(zip(locations, rates))})

with col2:
    st.dataframe(
        [{"Location": r[0], "Jobs": r[1], "Clean": r[2], "Success Rate": f"{r[3]}%"} for r in rows],
        use_container_width=True,
        hide_index=True,
    )

# --- Crew heat ---
st.header("Crew Heat")

rows = conn.execute("""
    SELECT nickname, heat, status FROM crew ORDER BY heat DESC
""").fetchall()

st.dataframe(
    [{"Nickname": r[0], "Heat": r[1], "Status": r[2]} for r in rows],
    use_container_width=True,
    hide_index=True,
)

conn.close()
