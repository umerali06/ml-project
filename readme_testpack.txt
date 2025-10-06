README — Test Pack (Sheets Model + CSVs + Guide)
Updated: 2025-10-04 01:52

[FR] — Mode d'emploi rapide
1) Importer le modèle dans Google Sheets :
   - Google Drive → Nouveau → Importer → téléverser "Google_Sheets_Model_Priority.xlsx"
   - Ouvrir dans Google Sheets.
2) Tester avec les CSV :
   - Fichier → Importer → Télécharger → choisir un CSV (basic ou extended).
   - Vérifier les colonnes : vehicle_id, zone_name, latitude, longitude, soc_now, hour, day_of_week, demand_zone_score.
3) Générer le Top‑50 :
   - Onglet TOP50 → coller la formule en A5 :
     =QUERY(SORT(DATA!A2:N, DATA!N2:N, FALSE), "select * limit 50", 0)
4) Guide Word :
   - Ouvrir "Guide_tests_CSV_AI_pilot_FR.docx" pour les formules (Haversine, mins_to_20%, priority_score) et conseils.
5) Données "extended" (pour notebook) :
   - Les fichiers extended contiennent timestamp_iso, temp_c, rain_mm, battery_health, trips_last_24h, avg_trip_km, last_trip_km, last_trip_min, minutes_to_empty.
   - Idéal pour tester un petit modèle dans Google Colab.

[EN] — Quick Start
1) Import the model into Google Sheets:
   - Google Drive → New → Import → upload "Google_Sheets_Model_Priority.xlsx"
   - Open in Google Sheets.
2) Test with the CSV files:
   - File → Import → Upload → pick any CSV (basic or extended).
   - Check headers: vehicle_id, zone_name, latitude, longitude, soc_now, hour, day_of_week, demand_zone_score.
3) Generate Top‑50:
   - TOP50 tab → paste this in A5:
     =QUERY(SORT(DATA!A2:N, DATA!N2:N, FALSE), "select * limit 50", 0)
4) Usage guide:
   - Open "Guide_tests_CSV_AI_pilot_FR.docx" for formulas (Haversine, mins_to_20%, priority_score) and tips.
5) Extended data (for notebooks):
   - Extended CSVs include timestamp_iso, temp_c, rain_mm, battery_health, trips_last_24h, avg_trip_km, last_trip_km, last_trip_min, minutes_to_empty.
   - Great for a small model test in Google Colab.

Pack contents
- Google_Sheets_Model_Priority.xlsx
- 6 CSV test files (basic + extended variants)
- Guide_tests_CSV_AI_pilot_FR.docx
- This README_TEST_PACK.txt

Contact
- Email: raykuate@prayaglobal.com
- Tel: 07 58 91 52 66

Notes
- All data is synthetic for development/testing only.
- Keep column headers unchanged if you want formulas to work without edits.
