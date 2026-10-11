# US Gateway Mathematics Outcomes Atlas

**Status:** Version 1.0, released 2026-10-10, verified by the maintainer | **Maintainer:** Faith Oluwafunmitan Esan, [ORCID 0009-0001-3694-157X](https://orcid.org/0009-0001-3694-157X) | **License:** code MIT, derived data and text CC BY 4.0

**In plain terms:** Passing a first college-level math class early is one of the strongest signs a community college student will finish a degree. Several states report this for each college, but every state publishes it differently and none of it is linked to the federal college records researchers use. This atlas does that matching once, carefully, for California and Texas, and publishes the result so anyone can look up a college or reuse the data.

New here? Read [docs/START_HERE.md](docs/START_HERE.md) first. Unfamiliar terms are explained in [docs/GLOSSARY.md](docs/GLOSSARY.md).

The atlas is an independent, curated resource that joins state course-level gateway mathematics outcome reporting (California Community Colleges Chancellor's Office metric 502C; Texas Higher Education Coordinating Board measure C18UC) to federal postsecondary data (IPEDS directory, enrollment and student aid) at the institution level, using hand-checked crosswalks from each state's reporting units to IPEDS UNITIDs. It is intended for institutional researchers, state policy analysts and education researchers who need gateway math outcomes in a form that can be joined to other federal data.

## Headline numbers

<!--STATS-->
- **California:** 115 colleges. Across the 2023 cohort, 71,574 of 348,509 students (20.5%) passed transfer-level math in their first year. The middle college's rate was 20.4%; one in ten colleges was below 11.6% and one in ten above 30.7%.
- **Texas:** 55 colleges. Across the 2022 cohort, 38,455 of 79,069 students (48.6%) passed a college-level math course within two years. The middle college's rate was 49.3%; one in ten colleges was below 35.2% and one in ten above 57.6%.

Numbers come from `report/stats.json`, written by `code/03_qa.py`.

## What is here

```
code/                 numbered scripts in run order, plus build_lib.py
data/raw/             federal inputs as fetched, with PROVENANCE.txt (state raw files are not redistributed; see below)
data/crosswalks/      state reporting unit -> IPEDS UNITID tables, with match notes
data/processed/       atlas tables, qa_report.txt, build_log.json
report/               stats.json, figures/, atlas/index.html (the web atlas)
docs/                 START_HERE, GLOSSARY, BUILD_SPEC, CODEBOOK, LIMITATIONS, VERIFY_CHECKLIST, NEXT_STEPS, TALK_TRACK
```

## Run it

Python 3.10 or newer, with `matplotlib`.

```
pip install matplotlib
python code/02_build.py      # match and combine
python code/03_qa.py         # quality checks and report/stats.json
python code/04_figures.py    # figures
python code/05_atlas.py      # the web atlas
python code/06_docs.py       # fills the numbers into this README
```

### Getting the state files

The state agencies do not attach an open license to their downloads, so this repository does not redistribute their raw files. To rebuild from scratch, download them yourself (about one hour, all public, no account needed) and place them as listed in `data/raw/PROVENANCE.txt`:

1. **California.** At https://datavista.cccco.edu/exports/new choose Data View "General Admit Cohort", years 19-20 to 23-24, Locale Type "College", one college at a time, format CSV. Save each file into `data/raw/ca/college/` named `gma_ca_college_<locale id>_<file name>`. The locale IDs are in `data/crosswalks/crosswalk_ca.csv`.
2. **Texas.** The atlas uses the tables shown at https://www.txhigheredaccountability.org/AcctPublic/ under Public Two-Year Colleges > Community Colleges > C18UC (reports 1184 and 1185), retrieved for every listed institution. `docs/NEXT_STEPS.md` describes a script to automate this in version 2.0.

Federal inputs are included in `data/raw/federal/` under the ODC Attribution License.

## Sources

| Source | Vintage | Terms | Accessed |
|---|---|---|---|
| CCCCO Data Vista, General Admit Cohort, metric 502C, https://datavista.cccco.edu/ | school years 2019-20 to 2023-24 | Copyright CCCCO; no open license stated; factual figures republished with attribution | 2026-10-10 |
| THECB Accountability System, measure C18UC, https://www.txhigheredaccountability.org/AcctPublic/ | cohorts 2020-2022 | Copyright THECB; no open license stated; factual figures republished with attribution | 2026-10-10 |
| IPEDS via Urban Institute Education Data Portal v0.27.0, https://educationdata.urban.org/documentation/ | directory and fall enrollment 2023; student aid 2021-22 | ODC Attribution License | 2026-10-10 |
| us-atlas 3.0.1 state outlines (US Census Bureau) | 2017 boundaries | ISC | 2026-10-10 |

## Limitations

See [docs/LIMITATIONS.md](docs/LIMITATIONS.md) before using or citing anything here. Most important: California and Texas measure different things, so their rates must not be compared.

## Citation

See `CITATION.cff`. DOI: added here once the Zenodo archive is created.

## AI assistance

Data collection scripting, matching drafts, code and document drafting were done with AI assistance (Claude, Anthropic). The maintainer made the analytic decisions and verified the figures listed in `docs/VERIFY_CHECKLIST.md`.
