import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

st.set_page_config(page_title="Roadmap (6–18 months) — Three Phases", layout="wide")
st.title("Roadmap for Implementation — 6–18 months (concise)")

# Start date input
start_date = st.date_input("Roadmap start date", value=datetime.date.today())
s = pd.to_datetime(start_date)

# Phase definitions
phases = [
    {
        "id": "Phase 1 (Months 0–3)",
        "name": "Diagnostics & Mobilization",
        "start": s,
        "end": s + pd.DateOffset(months=3),
        "explanation": (
            "Rapid asset & institutional diagnosis for priority municipalities (Aguascalientes, "
            "Tequisquiapan, Zapotitlán de Méndez). Formalize governance, validate network maps, "
            "and secure preliminary budgets to enable Phase 2."
        ),
        "milestones": [
            "Formalize a governance & project committee",
            "Detailed technical inspections & asset validation (km validated)",
            "GIS update and asset register approval",
            "Approve preliminary intervention budgets"
        ],
        "lead_actors": [
            "Municipal Water Utility (OOAPAS)", "State Water Commission (CEA)",
            "Municipal Public Works & Planning"
        ],
        "monitoring": {
            "% assets inspected": "target ≥ 80%",
            "Validated km (baseline)": "record km per utility",
            "Baseline best-practice probability": {
                "Aguascalientes": 0.0001,
                "Tequisquiapan": 0.1182,
                "Zapotitlán de Méndez": 0.4953,
                "Naucalpan": 0.9642
            }
        },
        "budget": {
            "surveys & inspections": "MXN 0.8M–1.6M",
            "GIS & asset register updates": "MXN 0.4M–0.8M",
            "mobilization / short-term staffing": "MXN 0.3M–0.6M",
            "phase_total": "MXN 1.5M–3.0M"
        },
        "contingencies": [
            "If inspection capacity limited >>> hire short-term field contractors or academic partners.",
            "If municipal approval delayed >>> apply conditional state matching funds or re-scope lowest-cost diagnostic."
        ]
    },
    {
        "id": "Phase 2 (Months 3–9)",
        "name": "Implementation — Priority Interventions",
        "start": s + pd.DateOffset(months=3),
        "end": s + pd.DateOffset(months=9),
        "explanation": (
            "Targeted network rehabilitation, staff reinforcement and metering plus selective pluvial works. "
            "Focus on municipalities with large feasible gains and low best-practice probability (Tequisquiapan, Aguascalientes)."
        ),
        "milestones": [
            "Execute targeted conduction & distribution rehabilitation contracts",
            "Recruit / reallocate ~15–20 technicians (+1 SD) and deploy operational kits",
            "Deploy selective pluvial drainage works to increase coverage by ~10 pp where feasible",
            "Meter procurement & rollout (1,000–5,000 units) and cost-recovery pilot"
        ],
        "lead_actors": [
            "Utility Technical Division", "Private civil works & meter-installation contractors",
            "State Water Commission (financing support)"
        ],
        "monitoring": {
            "Km rehabilitated (conduction)": "monthly cumulative",
            "Km rehabilitated (distribution)": "monthly cumulative",
            "Meters installed": "cumulative",
            "Pluvial coverage %": "measured at 3-month intervals",
            "Updated best-practice probability": "recompute at month 6"
        },
        "budget": {
            "network_rehab_conduction": "MXN 1M–6M (example: 3–40 km @ MXN150k/km)",
            "network_rehab_distribution": "MXN 2M–14M (example: 20–140 km @ MXN100k/km)",
            "pluvial_works": "MXN 3M–12M (scale dependent @ MXN100k–150k/km)",
            "metering_program": "MXN 1M–6M (1k–5k meters @ MXN500–1,200 each)",
            "staffing & training": "MXN 0.2M–1.0M",
            "phase_total": "MXN 9M–38M"
        },
        "contingencies": [
            "If budgets short >>> prioritize interventions delivering highest km per MXN (VfM) and pilot in highest-probability municipalities.",
            "If contractor shortage >>> use inter-municipal technical brigades or temporary outsourcing to certified firms."
        ]
    },
    {
        "id": "Phase 3 (Months 9–18)",
        "name": "Institutionalization & Scaling",
        "start": s + pd.DateOffset(months=9),
        "end": s + pd.DateOffset(months=18),
        "explanation": (
            "Embed monitoring, SOPs and budget lines to maintain rehabilitation gains. Scale successful pilots and integrate staffing and metering into recurrent budgets."
        ),
        "milestones": [
            "Standardize monitoring dashboards (NRW, meters per connection, km rehab)",
            "Publish operational manuals and O&M schedules",
            "Sign peer-learning agreements and scale funding allocations"
        ],
        "lead_actors": [
            "State Water Secretariat", "Municipal utilities", "Training & certification centers"
        ],
        "monitoring": {
            "NRW reduction": "annual % change",
            "% metered connections": "annual",
            "Annual km rehabilitated": "annual",
            "Sustained best-practice probability": "annual re-evaluation"
        },
        "budget": {
            "dashboard & IT systems": "MXN 0.5M–1.5M",
            "training & institutionalization": "MXN 0.5M–2.0M",
            "scaling pilot interventions": "MXN 1M–2.5M",
            "phase_total": "MXN 2M–6M"
        },
        "contingencies": [
            "If political turnover threatens continuity >>> embed actions in municipal POA and state-level agreements and publish dashboards for transparency.",
            "If recurrent funds missing >>> secure multi-year commitments or ringfence metering-derived revenues to finance operations."
        ]
    }
]

# Gantt 
st.subheader("Gantt: Phases & key milestones")
gantt_rows = []
for ph in phases:
    gantt_rows.append({
        "Task": ph["id"] + " — " + ph["name"],
        "Start": ph["start"].date(),
        "Finish": ph["end"].date(),
        "Type": "Phase"
    })
    # 1–2 key milestones as sub-rows for visual clarity
    mid = ph["start"] + (ph["end"] - ph["start"]) / 2
    gantt_rows.append({
        "Task": ph["id"] + " — Key: " + ph["milestones"][0],
        "Start": ph["start"].date(),
        "Finish": (ph["start"] + pd.DateOffset(days=10)).date(),
        "Type": "Milestone"
    })
    gantt_rows.append({
        "Task": ph["id"] + " — Key: " + ph["milestones"][-1],
        "Start": (ph["end"] - pd.DateOffset(days=10)).date(),
        "Finish": ph["end"].date(),
        "Type": "Milestone"
    })

gantt_df = pd.DataFrame(gantt_rows)
fig = px.timeline(gantt_df, x_start="Start", x_end="Finish", y="Task", color="Type",
                  category_orders={"Type": ["Phase", "Milestone"]})
fig.update_yaxes(autorange="reversed")
fig.update_layout(height=520, margin={"l":300, "r":20, "t":30, "b":20})
st.plotly_chart(fig, use_container_width=True)

# Summary table 
st.subheader("Summary table")
summary_rows = []
for ph in phases:
    summary_rows.append({
        "Phase": ph["id"],
        "Timeframe": f"{ph['start'].date()} : {ph['end'].date()}",
        "Top milestones (3)": "; ".join(ph["milestones"][:3]),
        "Lead actors": ", ".join(ph["lead_actors"]),
        "Key KPIs": "; ".join([f"{k}: {v}" for k, v in list(ph["monitoring"].items())[:2]]),
        "Budget (range)": ph["budget"].get("phase_total", "")
    })
st.dataframe(pd.DataFrame(summary_rows), height=240)

# Phase cards
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("Phases - concise explanations & highlights")
    for ph in phases[:2]:
        st.markdown(f"### {ph['id']} — {ph['name']}")
        st.write(ph['explanation'])
        st.markdown("**Milestones:**")
        for m in ph['milestones']:
            st.write(f"- {m}")
        st.markdown("**Lead actors:** " + ", ".join(ph['lead_actors']))
        st.markdown("**Monitoring indicators (key):**")
        for k, v in ph['monitoring'].items():
            st.write(f"- {k}: {v}")
        st.markdown("**Budget (major items):**")
        for k, v in ph['budget'].items():
            st.write(f"- {k}: {v}")
        st.markdown("**Contingencies:**")
        for c in ph['contingencies']:
            st.write(f"- {c}")
        st.markdown("---")

with col2:
    # Show phase 3 in parallel
    ph = phases[2]
    st.markdown(f"### {ph['id']} - {ph['name']}")
    st.write(ph['explanation'])
    st.markdown("**Milestones:**")
    for m in ph['milestones']:
        st.write(f"- {m}")
    st.markdown("**Lead actors:** " + ", ".join(ph['lead_actors']))
    st.markdown("**Monitoring indicators (key):**")
    for k, v in ph['monitoring'].items():
        st.write(f"- {k}: {v}")
    st.markdown("**Budget (major items):**")
    for k, v in ph['budget'].items():
        st.write(f"- {k}: {v}")
    st.markdown("**Contingencies:**")
    for c in ph['contingencies']:
        st.write(f"- {c}")
    st.markdown("---")