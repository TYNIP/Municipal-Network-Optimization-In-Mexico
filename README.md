# Infrastructure Prioritization Matrix

This tool evaluates interventions using a ***prioritization matrix*** with four criteria:
- **Impact on service**
- **Cost**
- **Feasibility**
- **Time-to-benefit**

You can adjust scores, apply **criteria weighting**, visualize results with **radar plots**, and
export the full matrix to **Excel**.

---

### Interventions Proposal

1. Based on the modeling results, a first intervention is a targeted network rehabilitation program focused on municipalities with large potential extension gains and low best-practice probability, such as Tequisquiapan (probability 0.1182) and Aguascalientes (0.0001). Our conductance and distribution models estimate that municipalities with higher total_tecnicos_y_operativos_hombres and tomas cubiertas exhibit significantly higher restoration capacity—e.g., a 1-SD increase in technical staff raises conduction rehab by +3.75 km, while a 1-SD increase in tomas cubiertas increases distribution rehab by +19.71 km. Thus, a modest staffing reinforcement (e.g., +1 SD equivalent increase of 15–20 technicians) is expected to increase feasible rehabilitation by 3–20 km, translating monetarily to MXN 1.0–6.0 million in avoided emergency repairs using your unit costs (MXN 150,000/km for conduction; MXN 100,000/km for distribution). Required inputs include short-term hiring or reallocation and operational kits; barriers include budget availability and the low baseline institutional probability of best-practice execution (as low as 0–12% in these municipalities).

2. A second intervention is selective pluvial drainage improvement, especially where the Logit model indicates strong predictor sensitivity to drainage coverage. The most influential predictor—porcentaje con drenaje (coef = +0.0381, p < 10⁻¹⁸)—means that raising drainage coverage by 10 percentage points increases the log-odds of best-practice performance by +0.381, roughly equivalent to increasing best-practice probability by 12–18 percentage points, depending on baseline probability. This directly benefits municipalities like Zapotitlán de Méndez (0.4953), which sits at the improvement threshold: raising coverage from (hypothetical) 70% to 80% could push it above 60–65% best-practice probability. The required inputs are pipe installation (average unit cost from your conduction/distribution model: MXN 100k–150k per km) and expanded household connections; barriers include urban topography and right-of-way constraints.

3. A third intervention is a cost-recovery and metering strategy, aimed at municipalities where total_sin_medidor shows a strong negative impact on performance—a 1-SD increase reduces conduction rehab by −3.01 km and distribution rehab by −8.51 km. Municipalities with high non-metered shares lose operational capacity and revenue, reducing staffing and investment room. Reducing unmetered connections by one standard deviation would be expected to recover between 3 and 8 km of feasible rehabilitation capacity, equal to MXN 300k–1.2M in capital savings. Inputs include procurement of household meters (~MXN 500–1200 per unit) and installation teams; barriers include household compliance and tariff politics.

---

## Scoring Rublic
            
| Score | Meaning |
|-------|---------|
| **5** | Excellent — high impact, very low cost, highly feasible, immediate benefits |
| **4** | Strong — significant benefits, reasonable cost |
| **3** | Moderate — useful impact, moderate cost, feasible with some constraints |
| **2** | Weak — limited impact or rising costs, delayed benefits |
| **1** | Very low — minimal impact, major barriers, high cost, long-term |
            
---