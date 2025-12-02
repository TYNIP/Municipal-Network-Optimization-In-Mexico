import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="Prioritization Matrix", layout="wide")

# Description
st.title("Infrastructure Prioritization Matrix")

st.markdown("""
### Data preparation and initial exploratory analysis
**Authors:** Arturo Cesar Morales Montaño, Alejandro Benavides Robledok, Víctor René Villafáñez Bárcena, Natalia Desirée Camargo Pérez

**Teacher:** Martín Flegl, Félix Eduardo Bueno Pascual

---
""")

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

st.markdown("""
### Interventions Proposal

1. Based on the modeling results, a first intervention is a targeted network rehabilitation program focused on municipalities with large potential extension gains and low best-practice probability, such as Tequisquiapan (probability 0.1182) and Aguascalientes (0.0001). Our conductance and distribution models estimate that municipalities with higher total_tecnicos_y_operativos_hombres and tomas cubiertas exhibit significantly higher restoration capacity—e.g., a 1-SD increase in technical staff raises conduction rehab by +3.75 km, while a 1-SD increase in tomas cubiertas increases distribution rehab by +19.71 km. Thus, a modest staffing reinforcement (e.g., +1 SD equivalent increase of 15–20 technicians) is expected to increase feasible rehabilitation by 3–20 km, translating monetarily to MXN 1.0–6.0 million in avoided emergency repairs using your unit costs (MXN 150,000/km for conduction; MXN 100,000/km for distribution). Required inputs include short-term hiring or reallocation and operational kits; barriers include budget availability and the low baseline institutional probability of best-practice execution (as low as 0–12% in these municipalities).

2. A second intervention is selective pluvial drainage improvement, especially where the Logit model indicates strong predictor sensitivity to drainage coverage. The most influential predictor—porcentaje con drenaje (coef = +0.0381, p < 10⁻¹⁸)—means that raising drainage coverage by 10 percentage points increases the log-odds of best-practice performance by +0.381, roughly equivalent to increasing best-practice probability by 12–18 percentage points, depending on baseline probability. This directly benefits municipalities like Zapotitlán de Méndez (0.4953), which sits at the improvement threshold: raising coverage from (hypothetical) 70% to 80% could push it above 60–65% best-practice probability. The required inputs are pipe installation (average unit cost from your conduction/distribution model: MXN 100k–150k per km) and expanded household connections; barriers include urban topography and right-of-way constraints.

3. A third intervention is a cost-recovery and metering strategy, aimed at municipalities where total_sin_medidor shows a strong negative impact on performance—a 1-SD increase reduces conduction rehab by −3.01 km and distribution rehab by −8.51 km. Municipalities with high non-metered shares lose operational capacity and revenue, reducing staffing and investment room. Reducing unmetered connections by one standard deviation would be expected to recover between 3 and 8 km of feasible rehabilitation capacity, equal to MXN 300k–1.2M in capital savings. Inputs include procurement of household meters (~MXN 500–1200 per unit) and installation teams; barriers include household compliance and tariff politics.

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
