# Mini AI Pilot — CSV → Prediction → Prioritized Dispatch

**Updated:** 2025-10-03 08:04

This bundle lets a beginner (even with no coding background) produce a **priority dispatch list** from a simple CSV.
Two ways to work:
- **No‑code (Google Sheets)** with formulas
- **One‑click Colab** notebook (press “Run all”)

---

## Files in this bundle

- **Full specs (Word)** → `Fiverr_Gig_Full_Specs_EN.docx`
- **Beginner Colab notebook** → `mini_ai_pilot_colab.ipynb`
- **Blank CSV template** (correct headers) → `gbfs_template.csv`

### Optional examples (if present)
- `synthetic_gbfs.csv` — synthetic dataset sample
- `dispatch_list.csv` — example prioritized output
- `model_metrics.txt` — example metrics
- `AI_roadmap_one_pager_FR.txt` — short French roadmap
- `Volunteer_Announcement_EN.docx`, `Fiverr_SOW_Mini_AI_Pilot_EN.docx` — recruiting & SOW extras

---

## How to use (Colab route)

1. Open **https://colab.research.google.com** → **File > Upload Notebook** → choose `mini_ai_pilot_colab.ipynb`.
2. Click **Runtime > Run all**.
3. Download `dispatch_list.csv` and `synthetic_gbfs.csv` from the left **Files** panel.
4. Open `dispatch_list.csv` in Google Sheets and sort/filter as needed.

**Replace with your data:** export your own CSV matching `gbfs_template.csv` headers and adapt the notebook to read your file instead of the synthetic one.

---

## How to use (No‑code Sheets route)

1. Create a Google Sheet with headers:
   `vehicle_id | zone_name | latitude | longitude | soc_now | hour | day_of_week | demand_zone_score`

2. Add **Hub_Lat** and **Hub_Lon** in two cells (e.g., K2 and L2).

3. **Distance to hub** (Haversine; adapt cell refs):
```excel
=LET(
  lat1,RADIANS($K$2), lon1,RADIANS($L$2),
  lat2,RADIANS(C2),  lon2,RADIANS(D2),
  dphi,lat2-lat1, dlambda,lon2-lon1,
  a,SIN(dphi/2)^2 + COS(lat1)*COS(lat2)*SIN(dlambda/2)^2,
  2*6371*ASIN(SQRT(a))
)
```

4. **Minutes to 20% (simple estimate)** (if E = soc_now):
```excel
=(E2 * 360) * ((E2 - 0.20) / E2)
```

5. **Priority score** (normalize components first if needed):
- `0.60 × (1 − norm(minutes_to_20))`
- `+ 0.25 × norm(demand_zone_score)`
- `+ 0.15 × (1 − norm(dist_to_hub))`

Sort **priority_score Z→A** to get the **Top‑50**.

---

## Acceptance criteria

- Notebook runs in free Colab (no paid APIs).
- On synthetic data: **MAE ≤ 35 min**, **R² ≥ 0.55**.
- `dispatch_list.csv` has required columns and the priority rule applied.
- Re-runnable with any CSV that keeps the same headers.
- README and short report supplied.

---

## Deliverables checklist

- `.ipynb` notebook (runnable end‑to‑end)
- `dispatch_list.csv` (+ optional **Top‑50** tab or CSV)
- Feature importances chart (png) — if model used
- Short **README** and **1‑page report**

---

## Legal & IP

- **NDA** required before work starts.
- **Full IP assignment** of code and outputs to buyer.
- No public portfolio use without written consent.

**Contact:** raykuate@prayaglobal.com · Tel: 07 58 91 52 66
