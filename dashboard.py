import sqlite3
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Art Crime Ledger", page_icon="🎨", layout="wide")

# ── Palette ────────────────────────────────────────────────────────
FOREST   = "#1a3d2e"
LIME     = "#c8f04a"
LAVENDER = "#c5b8f0"
BLUE     = "#b8d4f0"
PINK     = "#f0b8c8"
CREAM    = "#f0ead8"
CARD     = "#1f4a38"
BORDER   = "#2a5940"

PASTEL = [LAVENDER, BLUE, PINK]

# ── CSS injection ──────────────────────────────────────────────────
st.markdown(f"""
<style>
  /* Page background */
  .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
      background-color: {FOREST};
  }}
  .main .block-container {{
      background-color: {FOREST};
      padding-top: 1.5rem;
      max-width: 1400px;
  }}

  /* Sidebar */
  [data-testid="stSidebar"] {{
      background-color: {CARD};
      border-right: 1px solid {BORDER};
  }}
  [data-testid="stSidebar"] * {{
      color: {CREAM} !important;
  }}

  /* Global text */
  html, body, p, span, div, label {{
      color: {CREAM};
  }}
  h1, h2, h3, h4, h5, h6 {{
      color: {CREAM} !important;
  }}

  /* Section label */
  .sec-label {{
      color: {LIME};
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      border-bottom: 1px solid {LIME}38;
      padding-bottom: 7px;
      margin-bottom: 18px;
      margin-top: 4px;
  }}

  /* Metric card */
  .kpi-card {{
      background: {CARD};
      border: 1px solid {BORDER};
      border-radius: 10px;
      padding: 20px 18px 16px;
      text-align: center;
  }}
  .kpi-label {{
      color: {CREAM}80;
      font-size: 0.68rem;
      letter-spacing: 0.13em;
      text-transform: uppercase;
      margin-bottom: 8px;
  }}
  .kpi-value {{
      color: {LIME};
      font-size: 1.55rem;
      font-weight: 700;
      line-height: 1;
      letter-spacing: -0.01em;
      white-space: nowrap;
  }}
  .kpi-sub {{
      color: {CREAM}50;
      font-size: 0.7rem;
      margin-top: 5px;
      letter-spacing: 0.06em;
  }}

  /* Data tables */
  .ledger-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.875rem;
  }}
  .ledger-table th {{
      background: {LIME};
      color: {FOREST};
      font-weight: 700;
      font-size: 0.68rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 10px 15px;
      text-align: left;
  }}
  .ledger-table td {{
      color: {CREAM};
      padding: 9px 15px;
      border-bottom: 1px solid {BORDER};
  }}
  .ledger-table tr:nth-child(odd)  td {{ background: {FOREST}; }}
  .ledger-table tr:nth-child(even) td {{ background: {CARD};   }}
  .ledger-table tr:hover           td {{ background: {BORDER}  !important; cursor: default; }}

  /* Chart wrapper */
  [data-testid="stPlotlyChart"] {{
      border-radius: 10px;
      border: 1px solid {BORDER};
      overflow: hidden;
  }}

  /* Divider */
  .sec-hr {{
      border: none;
      border-top: 1px solid {BORDER};
      margin: 28px 0;
  }}

  /* Hide Streamlit chrome */
  #MainMenu, footer {{ visibility: hidden; }}
  [data-testid="stDecoration"] {{ display: none; }}
</style>
""", unsafe_allow_html=True)


# ── Chart style helper ─────────────────────────────────────────────
def _style(fig, ytitle=""):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=CARD,
        font_color=CREAM,
        font_family="'Segoe UI', 'Inter', sans-serif",
        margin=dict(l=12, r=12, t=18, b=12),
        yaxis_title=ytitle,
        xaxis=dict(gridcolor=BORDER, linecolor=BORDER, tickfont=dict(color=CREAM), title=""),
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, tickfont=dict(color=CREAM)),
        showlegend=False,
        bargap=0.32,
    )
    return fig


def html_table(headers, rows):
    ths = "".join(f"<th>{h}</th>" for h in headers)
    tds = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    return f'<table class="ledger-table"><thead><tr>{ths}</tr></thead><tbody>{tds}</tbody></table>'


def heat_span(val):
    if val >= 80:
        color, label = "#ff6b6b", "CRITICAL"
    elif val >= 55:
        color, label = PINK,     "HIGH"
    elif val >= 30:
        color, label = BLUE,     "ELEVATED"
    else:
        color, label = LIME,     "COOL"
    bar = (
        f'<span style="display:inline-block;width:{min(val, 100)}px;max-width:90px;'
        f'height:5px;background:{color};border-radius:3px;vertical-align:middle;'
        f'opacity:.65;margin-left:8px;"></span>'
    )
    tag = (
        f'<span style="color:{color};font-size:.65rem;letter-spacing:.09em;'
        f'margin-left:8px;opacity:.8;">{label}</span>'
    )
    return f'<span style="color:{color};font-weight:700;">{val}</span>{bar}{tag}'


def status_span(val):
    colors = {"active": LIME, "inactive": f"{CREAM}66", "burned": "#ff6b6b"}
    c = colors.get(val.lower(), LAVENDER)
    return f'<span style="color:{c};font-weight:600;letter-spacing:.06em;">{val.upper()}</span>'


# ── Database ───────────────────────────────────────────────────────
conn = sqlite3.connect("ledger.db")

# ── Page title ─────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding-bottom:1.5rem;">
  <div style="color:{LIME};font-size:2.1rem;font-weight:700;letter-spacing:.04em;line-height:1;">
    Art Crime Ledger
  </div>
  <div style="color:{CREAM}60;font-size:.78rem;letter-spacing:.18em;margin-top:5px;">
    OPERATIONS DASHBOARD
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI cards ──────────────────────────────────────────────────────
kpi = conn.execute("""
    SELECT
        COUNT(*)                                                             AS total_jobs,
        COALESCE(SUM(gross_take), 0)                                        AS gross_take,
        ROUND(100.0 * SUM(CASE WHEN outcome='clean' THEN 1 ELSE 0 END)
              / MAX(COUNT(*), 1), 1)                                         AS success_rate,
        COUNT(DISTINCT mark_id)                                              AS targets
    FROM jobs
""").fetchone()

active_crew = conn.execute(
    "SELECT COUNT(*) FROM crew WHERE status='active'"
).fetchone()[0]

kpi_data = [
    ("Total Operations",   kpi[0],                  "jobs in ledger"),
    ("Gross Take",         f"${kpi[1]:,.0f}",        "across all heists"),
    ("Success Rate",       f"{kpi[2]}%",             "clean outcomes"),
    ("Active Crew",        active_crew,              "operatives"),
    ("Unique Targets",     kpi[3],                   "artworks marked"),
]

cols = st.columns(5)
for col, (label, value, sub) in zip(cols, kpi_data):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<hr class="sec-hr">', unsafe_allow_html=True)

# ── Crew Earnings ──────────────────────────────────────────────────
st.markdown('<div class="sec-label">Crew Earnings</div>', unsafe_allow_html=True)

rows = conn.execute("""
    SELECT c.nickname, SUM(jc.payout) AS total_earned
    FROM job_crew jc
    JOIN crew c ON jc.crew_id = c.id
    GROUP BY c.nickname
    ORDER BY total_earned DESC
""").fetchall()

nicknames = [r[0] for r in rows]
earnings  = [r[1] for r in rows]
bar_colors = [LIME if i == 0 else PASTEL[i % 3] for i in range(len(nicknames))]

fig = go.Figure(go.Bar(
    x=nicknames,
    y=earnings,
    marker_color=bar_colors,
    marker_line_width=0,
    text=[f"${e:,.0f}" for e in earnings],
    textposition="outside",
    textfont=dict(color=CREAM, size=11),
    hovertemplate="%{x}<br>$%{y:,.0f}<extra></extra>",
))
st.plotly_chart(_style(fig, "Total Payout ($)"), use_container_width=True)

st.markdown('<hr class="sec-hr">', unsafe_allow_html=True)

# ── Most Targeted Artworks ─────────────────────────────────────────
st.markdown('<div class="sec-label">Most Targeted Artworks</div>', unsafe_allow_html=True)

rows = conn.execute("""
    SELECT m.title, COUNT(*) AS times_targeted
    FROM jobs j
    JOIN marks m ON j.mark_id = m.id
    GROUP BY m.title
    ORDER BY times_targeted DESC
""").fetchall()

titles = [r[0] for r in rows]
counts = [r[1] for r in rows]
bar_colors2 = [PASTEL[i % 3] for i in range(len(titles))]

fig2 = go.Figure(go.Bar(
    x=titles,
    y=counts,
    marker_color=bar_colors2,
    marker_line_width=0,
    text=counts,
    textposition="outside",
    textfont=dict(color=CREAM, size=11),
    hovertemplate="%{x}<br>%{y} job(s)<extra></extra>",
))
st.plotly_chart(_style(fig2, "Times Targeted"), use_container_width=True)

st.markdown('<hr class="sec-hr">', unsafe_allow_html=True)

# ── Museum Success Rates ───────────────────────────────────────────
st.markdown('<div class="sec-label">Success Rate by Museum</div>', unsafe_allow_html=True)

rows = conn.execute("""
    SELECT m.location,
           COUNT(*)                                                              AS total_jobs,
           SUM(CASE WHEN j.outcome = 'clean' THEN 1 ELSE 0 END)                AS clean_jobs,
           ROUND(100.0 * SUM(CASE WHEN j.outcome = 'clean' THEN 1 ELSE 0 END)
                 / COUNT(*), 1)                                                  AS success_rate
    FROM jobs j
    JOIN marks m ON j.mark_id = m.id
    GROUP BY m.location
    ORDER BY success_rate DESC
""").fetchall()

chart_col, table_col = st.columns([3, 2])

with chart_col:
    locations = [r[0] for r in rows]
    rates     = [r[3] for r in rows]
    rate_colors = [LIME if r >= 75 else BLUE if r >= 50 else PINK for r in rates]

    fig3 = go.Figure(go.Bar(
        x=locations,
        y=rates,
        marker_color=rate_colors,
        marker_line_width=0,
        text=[f"{r}%" for r in rates],
        textposition="outside",
        textfont=dict(color=CREAM, size=11),
        hovertemplate="%{x}<br>%{y}%<extra></extra>",
    ))
    fig3.update_layout(yaxis_range=[0, 115])
    st.plotly_chart(_style(fig3, "Success Rate (%)"), use_container_width=True)

with table_col:
    st.markdown("<br>", unsafe_allow_html=True)
    table_rows = [(r[0], r[1], r[2], f"{r[3]}%") for r in rows]
    st.markdown(
        html_table(["Location", "Jobs", "Clean", "Rate"], table_rows),
        unsafe_allow_html=True,
    )

st.markdown('<hr class="sec-hr">', unsafe_allow_html=True)

# ── Crew Heat ──────────────────────────────────────────────────────
st.markdown('<div class="sec-label">Crew Heat Levels</div>', unsafe_allow_html=True)

rows = conn.execute(
    "SELECT nickname, heat, status FROM crew ORDER BY heat DESC"
).fetchall()

table_rows = [
    (r[0], heat_span(r[1]), status_span(r[2]))
    for r in rows
]
st.markdown(
    html_table(["Operative", "Heat", "Status"], table_rows),
    unsafe_allow_html=True,
)

conn.close()
