"""Step 7: write docs/VERIFY_CHECKLIST.md with this build's real rows and numbers.

Plain-language note: generates your checking list. Every item names a file,
a row, a value, and exactly where to confirm it on the state's own website.
"""
import json
import random

import build_lib as b

long = b.read_csv(b.OUT / "atlas_v1_long.csv")
cols = b.read_csv(b.OUT / "atlas_v1_colleges.csv")
stats = json.load(open(b.ROOT / "report" / "stats.json"))
p = lambda v: f"{float(v)*100:.1f}%"

CA_HOW = ("Go to https://datavista.cccco.edu/data_views/single_metric_first_time_nsa . Under LOCALE choose College, then "
          "**{src}**. Under METRIC choose 502C (Completed Transfer-Level Math in the First Year). Hover the point for school year **{sy}**.")
TX_HOW = ("Go to https://www.txhigheredaccountability.org/AcctPublic/ , click PUBLIC TWO-YEAR COLLEGES > Community Colleges, "
          "choose **{src}** in the institution list, open Completion, then **C18UC - Underprepared/Prepared Students**. "
          "In the Prepared and Underprepared 'Completing a College Level Course' tables, Math row, column **{c}**.")


def item(r):
    if r["state"] == "CA":
        sy = f"{r['cohort'][2:]}-{int(r['cohort'][2:]) + 1:02d}"
        how = CA_HOW.format(src=r["state_source_name"], sy=sy)
        exp = f"It should show {r['completed_n']} of {r['cohort_n']} ({p(r['rate'])})."
    else:
        how = TX_HOW.format(src=r["state_source_name"], c=r["cohort"])
        exp = (f"Prepared: {r['prepared_completed_n']} completed of {r['prepared_n']}. Underprepared: "
               f"{r['underprepared_completed_n']} of {r['underprepared_n']}. Together {r['completed_n']} of {r['cohort_n']} = {p(r['rate'])}.")
    return (f"- [ ] **{r['ipeds_name']}** ({r['state']}), cohort {r['cohort']}. File `data/processed/atlas_v1_long.csv`, "
            f"row where `unitid` = {r['unitid']} and `cohort` = {r['cohort']}. {how} {exp} ___")


def pick(state, name, cohort=None):
    rs = [r for r in long if r["state"] == state and r["ipeds_name"] == name]
    rs.sort(key=lambda r: r["cohort"])
    return rs[-1] if rs else None


L = []
a = L.append
a("# Your verification checklist\n")
a("*Plain-language version: before anything goes public under your name, you check it. Every item below names the exact file, row and value, and where to confirm it on the state's own website. Total time: about 1.5 to 2 hours. Tick each box and add the date. The publish gate checks the mechanical items automatically; these are yours.*\n")
a("## Part 1: Make sure the results can be rebuilt (15 to 30 min)\n")
a("Pick one:")
a("- [ ] **Option A, run it yourself.** In a terminal in the project folder, run: `pip install matplotlib` then `python code/02_build.py && python code/03_qa.py && python code/04_figures.py && python code/05_atlas.py && python code/06_docs.py`. The last lines should repeat the headline numbers below.")
a("- [ ] **Option B, ask Claude.** In a new chat with Opus 5.5 or Fable 5, upload the project folder and say: \"Re-run this pipeline from the raw files and give me the headline numbers.\" Compare with:\n")
for s in ["CA", "TX"]:
    x = stats[s]
    a(f"  - {s}: {x['colleges']} colleges; latest cohort {x['latest_cohort']}: {x['completers_latest_cohort']:,} of {x['students_latest_cohort']:,} = {p(x['pooled_rate_latest_cohort'])}; median college {p(x['median_college_rate'])}")
a("\n- [ ] Every number in the README and the report matches `report/stats.json`.\n")
a("## Part 2: Check the sources (15 min)\n")
a("- [ ] https://datavista.cccco.edu/ loads, and the Metric Definition Dictionary still defines 502C as in `docs/CODEBOOK.md`.")
a("- [ ] https://www.txhigheredaccountability.org/AcctPublic/ loads, and Measures and Definitions (Community Colleges) still defines C18UC as in `docs/CODEBOOK.md`.")
a("- [ ] https://educationdata.urban.org/documentation/ still states the ODC Attribution License under Data Policy and Terms of Use.")
a("- [ ] You have read the reuse note in `docs/LIMITATIONS.md` item 13 and decided (Part 4).\n")
a("## Part 3: Check rows by hand (45 to 60 min)\n")
a("**Five well-known colleges:**")
for s, n in [("CA", "East Los Angeles College"), ("CA", "Mt San Antonio College"), ("TX", "Austin Community College District"),
             ("TX", "Tarrant County College District"), ("TX", "Palo Alto College")]:
    r = pick(s, n)
    if r:
        a(item(r))
a("\n**Extremes (most likely to hide errors):**")
for s in ["CA", "TX"]:
    big = [c for c in cols if c["state"] == s and c["small_cohort"] == "0" and c["latest_rate"] != ""]
    for c in [min(big, key=lambda c: float(c["latest_rate"])), max(big, key=lambda c: float(c["latest_rate"]))]:
        a(item(pick(s, c["ipeds_name"])))
a("\n**Random rows (chosen by computer, seed 2026):**")
rnd = random.Random(2026)
for r in rnd.sample([r for r in long if r["completed_n"] != ""], 5):
    a(item(r))
a("\n**Matching checks.** Open `data/crosswalks/crosswalk_tx.csv` and `crosswalk_ca.csv`:")
a("- [ ] Houston: THECB lists 'Houston City College'; IPEDS 2023 lists 'Houston Community College' (UNITID 225423). Confirm these are the same institution (for example, the college's own website announcing the new name). ___")
a("- [ ] Lone Star College System (UNITID 227182) is matched to THECB's system-level row, because IPEDS reports Lone Star as one institution. Agree? ___")
a("- [ ] Skim the 14 California hand-matched names (`match_note` = 'hand-matched name variant'). Each pair is the same college. ___\n")
a("## Part 4: Your decisions (10 min)\n")
a("The build made these choices provisionally. Agree or change each one.\n")
a("- [ ] **Texas: add 'ready' and 'not ready' students together?** Texas does not publish one all-students number. A: add them (current). This gives one rate per college, closest to California's all-students cohort. B: show only the 'not ready' rate, which is the group corequisite reform targets, but leaves out most students at some colleges. Recommended: A, with both parts always shown. Your choice: ___")
a("- [ ] **Small-cohort threshold.** Rates from fewer than 30 students are flagged and drawn as dashed circles. A: keep 30. B: use 50, which flags a few more small rural colleges. Recommended: A. Your choice: ___")
a("- [ ] **Weatherford College 2021 (Texas).** THECB shows 12 students that year against more than 600 in the years around it. A: keep the published value, flagged (current). B: drop that cohort from Weatherford's pooled rate. Recommended: B, because one obviously incomplete year distorts the pooled rate; the long table still keeps it. Your choice: ___")
a("- [ ] **Texas cohort label.** THECB labels cohorts 2020, 2021, 2022. The atlas treats '2020' as students entering in summer/fall 2020. Confirm on THECB's C18UC definition page or the Interactive Guide. ___")
a("- [ ] **State data reuse.** Neither state attaches an open license. A: release now, republishing only counts and rates with attribution, without the raw files (current). B: first email each agency asking them to confirm (template in `docs/AGENCY_EMAIL.md`), then release. Recommended: B if you can wait about two weeks; A is common practice for published government statistics. This is not legal advice. Your choice: ___\n")
a("## Part 5: Before it goes public (15 to 30 min)\n")
a("- [ ] The README summary and the report abstract are rewritten in your own words. Nothing remains you could not explain or defend. (Claude can do this with you line by line.)")
a("- [ ] Your name, ORCID, affiliation and email are correct in `AUTHORS.json`.")
a("- [ ] You have read `docs/LIMITATIONS.md` and agree with it.")
a("- [ ] Draft stamps removed (Claude rebuilds with `--final`) and the publish gate passes.")
a("- [ ] Evidence log row written on release day.\n")
a("**When every box is ticked, tell Claude in your own words that you have checked the package and approve publishing.**")
(b.ROOT / "docs" / "VERIFY_CHECKLIST.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
