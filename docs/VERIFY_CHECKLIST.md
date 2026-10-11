# Your verification checklist

*Plain-language version: before anything goes public under your name, you check it. Every item below names the exact file, row and value, and where to confirm it on the state's own website. Total time: about 1.5 to 2 hours. Tick each box and add the date. The publish gate checks the mechanical items automatically; these are yours.*

## Part 1: Make sure the results can be rebuilt (15 to 30 min)

Pick one:
- [ ] **Option A, run it yourself.** In a terminal in the project folder, run: `pip install matplotlib` then `python code/02_build.py && python code/03_qa.py && python code/04_figures.py && python code/05_atlas.py && python code/06_docs.py`. The last lines should repeat the headline numbers below.
- [ ] **Option B, ask Claude.** In a new chat with Opus 5.5 or Fable 5, upload the project folder and say: "Re-run this pipeline from the raw files and give me the headline numbers." Compare with:

  - CA: 115 colleges; latest cohort 2023: 71,574 of 348,509 = 20.5%; median college 20.4%
  - TX: 55 colleges; latest cohort 2022: 38,455 of 79,069 = 48.6%; median college 49.3%

- [ ] Every number in the README and the report matches `report/stats.json`.

## Part 2: Check the sources (15 min)

- [ ] https://datavista.cccco.edu/ loads, and the Metric Definition Dictionary still defines 502C as in `docs/CODEBOOK.md`.
- [ ] https://www.txhigheredaccountability.org/AcctPublic/ loads, and Measures and Definitions (Community Colleges) still defines C18UC as in `docs/CODEBOOK.md`.
- [ ] https://educationdata.urban.org/documentation/ still states the ODC Attribution License under Data Policy and Terms of Use.
- [ ] You have read the reuse note in `docs/LIMITATIONS.md` item 13 and decided (Part 4).

## Part 3: Check rows by hand (45 to 60 min)

**Five well-known colleges:**
- [ ] **East Los Angeles College** (CA), cohort 2023. File `data/processed/atlas_v1_long.csv`, row where `unitid` = 113856 and `cohort` = 2023. Go to https://datavista.cccco.edu/data_views/single_metric_first_time_nsa . Under LOCALE choose College, then **East Los Angeles College**. Under METRIC choose 502C (Completed Transfer-Level Math in the First Year). Hover the point for school year **23-24**. It should show 676 of 7492 (9.0%). ___
- [ ] **Mt San Antonio College** (CA), cohort 2023. File `data/processed/atlas_v1_long.csv`, row where `unitid` = 119164 and `cohort` = 2023. Go to https://datavista.cccco.edu/data_views/single_metric_first_time_nsa . Under LOCALE choose College, then **Mt. San Antonio College**. Under METRIC choose 502C (Completed Transfer-Level Math in the First Year). Hover the point for school year **23-24**. It should show 1517 of 6646 (22.8%). ___
- [ ] **Austin Community College District** (TX), cohort 2022. File `data/processed/atlas_v1_long.csv`, row where `unitid` = 222992 and `cohort` = 2022. Go to https://www.txhigheredaccountability.org/AcctPublic/ , click PUBLIC TWO-YEAR COLLEGES > Community Colleges, choose **AUSTIN COMMUNITY COLLEGE** in the institution list, open Completion, then **C18UC - Underprepared/Prepared Students**. In the Prepared and Underprepared 'Completing a College Level Course' tables, Math row, column **2022**. Prepared: 1065 completed of 1568. Underprepared: 594 of 1315. Together 1659 of 2883 = 57.5%. ___
- [ ] **Tarrant County College District** (TX), cohort 2022. File `data/processed/atlas_v1_long.csv`, row where `unitid` = 228547 and `cohort` = 2022. Go to https://www.txhigheredaccountability.org/AcctPublic/ , click PUBLIC TWO-YEAR COLLEGES > Community Colleges, choose **TARRANT COUNTY COLLEGE DISTRICT** in the institution list, open Completion, then **C18UC - Underprepared/Prepared Students**. In the Prepared and Underprepared 'Completing a College Level Course' tables, Math row, column **2022**. Prepared: 1769 completed of 2897. Underprepared: 956 of 1843. Together 2725 of 4740 = 57.5%. ___
- [ ] **Palo Alto College** (TX), cohort 2022. File `data/processed/atlas_v1_long.csv`, row where `unitid` = 246354 and `cohort` = 2022. Go to https://www.txhigheredaccountability.org/AcctPublic/ , click PUBLIC TWO-YEAR COLLEGES > Community Colleges, choose **ALAMO CCD-PALO ALTO COLLEGE** in the institution list, open Completion, then **C18UC - Underprepared/Prepared Students**. In the Prepared and Underprepared 'Completing a College Level Course' tables, Math row, column **2022**. Prepared: 438 completed of 662. Underprepared: 443 of 1156. Together 881 of 1818 = 48.5%. ___

**Extremes (most likely to hide errors):**
- [ ] **Palo Verde College** (CA), cohort 2023. File `data/processed/atlas_v1_long.csv`, row where `unitid` = 120953 and `cohort` = 2023. Go to https://datavista.cccco.edu/data_views/single_metric_first_time_nsa . Under LOCALE choose College, then **Palo Verde College**. Under METRIC choose 502C (Completed Transfer-Level Math in the First Year). Hover the point for school year **23-24**. It should show 39 of 909 (4.3%). ___
- [ ] **Irvine Valley College** (CA), cohort 2023. File `data/processed/atlas_v1_long.csv`, row where `unitid` = 116439 and `cohort` = 2023. Go to https://datavista.cccco.edu/data_views/single_metric_first_time_nsa . Under LOCALE choose College, then **Irvine Valley College**. Under METRIC choose 502C (Completed Transfer-Level Math in the First Year). Hover the point for school year **23-24**. It should show 1295 of 3384 (38.3%). ___
- [ ] **Del Mar College** (TX), cohort 2022. File `data/processed/atlas_v1_long.csv`, row where `unitid` = 224350 and `cohort` = 2022. Go to https://www.txhigheredaccountability.org/AcctPublic/ , click PUBLIC TWO-YEAR COLLEGES > Community Colleges, choose **DEL MAR COLLEGE** in the institution list, open Completion, then **C18UC - Underprepared/Prepared Students**. In the Prepared and Underprepared 'Completing a College Level Course' tables, Math row, column **2022**. Prepared: 92 completed of 217. Underprepared: 97 of 592. Together 189 of 809 = 23.4%. ___
- [ ] **Howard College** (TX), cohort 2022. File `data/processed/atlas_v1_long.csv`, row where `unitid` = 225520 and `cohort` = 2022. Go to https://www.txhigheredaccountability.org/AcctPublic/ , click PUBLIC TWO-YEAR COLLEGES > Community Colleges, choose **HOWARD CJCD-HOWARD COLLEGE** in the institution list, open Completion, then **C18UC - Underprepared/Prepared Students**. In the Prepared and Underprepared 'Completing a College Level Course' tables, Math row, column **2022**. Prepared: 80 completed of 103. Underprepared: 143 of 219. Together 223 of 322 = 69.2%. ___

**Random rows (chosen by computer, seed 2026):**
- [ ] **College of the Sequoias** (CA), cohort 2020. File `data/processed/atlas_v1_long.csv`, row where `unitid` = 123217 and `cohort` = 2020. Go to https://datavista.cccco.edu/data_views/single_metric_first_time_nsa . Under LOCALE choose College, then **College of the Sequoias**. Under METRIC choose 502C (Completed Transfer-Level Math in the First Year). Hover the point for school year **20-21**. It should show 732 of 2956 (24.8%). ___
- [ ] **Los Medanos College** (CA), cohort 2021. File `data/processed/atlas_v1_long.csv`, row where `unitid` = 117894 and `cohort` = 2021. Go to https://datavista.cccco.edu/data_views/single_metric_first_time_nsa . Under LOCALE choose College, then **Los Medanos College**. Under METRIC choose 502C (Completed Transfer-Level Math in the First Year). Hover the point for school year **21-22**. It should show 605 of 2164 (28.0%). ___
- [ ] **Shasta College** (CA), cohort 2019. File `data/processed/atlas_v1_long.csv`, row where `unitid` = 123299 and `cohort` = 2019. Go to https://datavista.cccco.edu/data_views/single_metric_first_time_nsa . Under LOCALE choose College, then **Shasta College**. Under METRIC choose 502C (Completed Transfer-Level Math in the First Year). Hover the point for school year **19-20**. It should show 245 of 1711 (14.3%). ___
- [ ] **Skyline College** (CA), cohort 2019. File `data/processed/atlas_v1_long.csv`, row where `unitid` = 123509 and `cohort` = 2019. Go to https://datavista.cccco.edu/data_views/single_metric_first_time_nsa . Under LOCALE choose College, then **Skyline College**. Under METRIC choose 502C (Completed Transfer-Level Math in the First Year). Hover the point for school year **19-20**. It should show 477 of 1636 (29.2%). ___
- [ ] **Northeast Lakeview College** (TX), cohort 2021. File `data/processed/atlas_v1_long.csv`, row where `unitid` = 488730 and `cohort` = 2021. Go to https://www.txhigheredaccountability.org/AcctPublic/ , click PUBLIC TWO-YEAR COLLEGES > Community Colleges, choose **ALAMO CCD-NORTHEAST LAKEVIEW COLLEGE** in the institution list, open Completion, then **C18UC - Underprepared/Prepared Students**. In the Prepared and Underprepared 'Completing a College Level Course' tables, Math row, column **2021**. Prepared: 247 completed of 319. Underprepared: 221 of 426. Together 468 of 745 = 62.8%. ___

**Matching checks.** Open `data/crosswalks/crosswalk_tx.csv` and `crosswalk_ca.csv`:
- [ ] Houston: THECB lists 'Houston City College'; IPEDS 2023 lists 'Houston Community College' (UNITID 225423). Confirm these are the same institution (for example, the college's own website announcing the new name). ___
- [ ] Lone Star College System (UNITID 227182) is matched to THECB's system-level row, because IPEDS reports Lone Star as one institution. Agree? ___
- [ ] Skim the 14 California hand-matched names (`match_note` = 'hand-matched name variant'). Each pair is the same college. ___

## Part 4: Your decisions (10 min)

The build made these choices provisionally. Agree or change each one.

- [ ] **Texas: add 'ready' and 'not ready' students together?** Texas does not publish one all-students number. A: add them (current). This gives one rate per college, closest to California's all-students cohort. B: show only the 'not ready' rate, which is the group corequisite reform targets, but leaves out most students at some colleges. Recommended: A, with both parts always shown. Your choice: ___
- [ ] **Small-cohort threshold.** Rates from fewer than 30 students are flagged and drawn as dashed circles. A: keep 30. B: use 50, which flags a few more small rural colleges. Recommended: A. Your choice: ___
- [ ] **Weatherford College 2021 (Texas).** THECB shows 12 students that year against more than 600 in the years around it. A: keep the published value, flagged (current). B: drop that cohort from Weatherford's pooled rate. Recommended: B, because one obviously incomplete year distorts the pooled rate; the long table still keeps it. Your choice: ___
- [ ] **Texas cohort label.** THECB labels cohorts 2020, 2021, 2022. The atlas treats '2020' as students entering in summer/fall 2020. Confirm on THECB's C18UC definition page or the Interactive Guide. ___
- [ ] **State data reuse.** Neither state attaches an open license. A: release now, republishing only counts and rates with attribution, without the raw files (current). B: first email each agency asking them to confirm (template in `docs/AGENCY_EMAIL.md`), then release. Recommended: B if you can wait about two weeks; A is common practice for published government statistics. This is not legal advice. Your choice: ___

## Part 5: Before it goes public (15 to 30 min)

- [ ] The README summary and the report abstract are rewritten in your own words. Nothing remains you could not explain or defend. (Claude can do this with you line by line.)
- [ ] Your name, ORCID, affiliation and email are correct in `AUTHORS.json`.
- [ ] You have read `docs/LIMITATIONS.md` and agree with it.
- [ ] Draft stamps removed (Claude rebuilds with `--final`) and the publish gate passes.
- [ ] Evidence log row written on release day.

**When every box is ticked, tell Claude in your own words that you have checked the package and approve publishing.**
