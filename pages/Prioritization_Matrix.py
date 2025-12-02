import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="Prioritization Matrix", layout="wide")

# Description
st.title("Prioritization Matrix")

st.markdown("""
This tool evaluates interventions using a ***prioritization matrix*** with four criteria:
- **Impact on service**
- **Cost**
- **Feasibility**
- **Time-to-benefit**

You can adjust scores, apply **criteria weighting**, visualize results with **radar plots**, and
export the full matrix to **Excel**.

---
""")



# Scoring Rubric
st.markdown("""
## Scoring Rublic
            
| Score | Meaning |
|-------|---------|
| **5** | Excellent — high impact, very low cost, highly feasible, immediate benefits |
| **4** | Strong — significant benefits, reasonable cost |
| **3** | Moderate — useful impact, moderate cost, feasible with some constraints |
| **2** | Weak — limited impact or rising costs, delayed benefits |
| **1** | Very low — minimal impact, major barriers, high cost, long-term |
            
---
""")

# Default Interventions
default_data = {
    "Initiative": [
        "Targeted Network Rehabilitation",
        "Selective Pluvial Drainage Upgrades",
        "Cost-Recovery & Household Metering"
    ],
    "Impact": [5, 4, 3],
    "Cost": [3, 2, 4],
    "Feasibility": [3, 4, 5],
    "Time_to_Benefit": [4, 3, 3],
}

df = pd.DataFrame(default_data)

st.subheader("Step 1 — Score Each Initiative")
edited_df = st.data_editor(df, use_container_width=True)

# Weighting
st.subheader("Step 2 — Set Criteria Weights")

col1, col2, col3, col4 = st.columns(4)

weights = {
    "Impact": col1.slider("Impact Weight", 0.0, 1.0, 0.40),
    "Cost": col2.slider("Cost Weight", 0.0, 1.0, 0.20),
    "Feasibility": col3.slider("Feasibility Weight", 0.0, 1.0, 0.20),
    "Time_to_Benefit": col4.slider("Time-to-Benefit Weight", 0.0, 1.0, 0.20)
}

# Normalize weights automatically
total_w = sum(weights.values())
weights = {k: v / total_w for k, v in weights.items()}

# Weighted Score Calculation
st.subheader("Step 3 — Prioritization Matrix with Weighted Ranking")

df_calc = edited_df.copy()
df_calc["Weighted Score"] = (
    df_calc["Impact"] * weights["Impact"] +
    df_calc["Cost"] * weights["Cost"] +
    df_calc["Feasibility"] * weights["Feasibility"] +
    df_calc["Time_to_Benefit"] * weights["Time_to_Benefit"]
)

df_calc = df_calc.sort_values("Weighted Score", ascending=False).reset_index(drop=True)

st.dataframe(df_calc.style.background_gradient(cmap="Blues"), use_container_width=True)


# Radar Plot
st.subheader("Step 4 — Radar Plot Comparison")

initiative_selected = st.selectbox(
    "Select an initiative to visualize:",
    df_calc["Initiative"]
)

row = df_calc[df_calc["Initiative"] == initiative_selected].iloc[0]

categories = ["Impact", "Cost", "Feasibility", "Time_to_Benefit"]
values = [row[c] for c in categories]
values += values[:1]  # close the loop

fig = go.Figure(data=[
    go.Scatterpolar(
        r=values,
        theta=categories + [categories[0]],
        fill='toself',
        name=initiative_selected
    )
])

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Excel Export
st.subheader("Step 5 — Export Prioritization Matrix")

def convert_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Prioritization Matrix")
    return output.getvalue()

excel_data = convert_to_excel(df_calc)

st.download_button(
    label="Download Prioritization Matrix (Excel)",
    data=excel_data,
    file_name="prioritization_matrix.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
