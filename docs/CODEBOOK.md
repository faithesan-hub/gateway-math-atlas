# Codebook

*Plain-language note: this lists every column in the two atlas tables, what it means, and where it comes from. You will use it when checking rows by hand.*

## Files

| File | One row is | Rows |
|---|---|---|
| `data/processed/atlas_v1_long.csv` | one college, one starting cohort | see `qa_report.txt` |
| `data/processed/atlas_v1_colleges.csv` | one college (latest cohort plus a pooled 3-cohort rate) | see `qa_report.txt` |
| `data/crosswalks/crosswalk_ca.csv` | one California Data Vista college and its federal ID | 123 |
| `data/crosswalks/crosswalk_tx.csv` | one Texas THECB institution and its federal ID | 55 |

## Columns: `atlas_v1_long.csv`

| Column | Meaning | Source and transformation |
|---|---|---|
| `state` | CA or TX | |
| `unitid` | Federal IPEDS institution ID | Crosswalk |
| `ipeds_name` | Institution name as IPEDS lists it | IPEDS directory 2023, via Urban Institute Education Data Portal v0.27.0 |
| `state_source_id` | The state's own ID for the reporting unit | CA: Data Vista locale ID. TX: THECB Accountability System institution ID |
| `state_source_name` | The state's own name for the reporting unit | As published |
| `match_level` | `college` when the state reports the same unit IPEDS does; `district` when both report one multi-campus district or system as a single unit | Crosswalk |
| `cohort` | Starting cohort year. CA: first year of the school year the cohort started (2023 = 2023-24). TX: entering cohort year as labeled by THECB | THECB labels each cohort by its entry year (summer/fall); checked by the maintainer |
| `measure_code` | The state's measure | CA: CCCCO metric 502C. TX: THECB measure C18UC, math rows, reports 1184 and 1185 combined |
| `measure_window` | Time allowed to pass the course | CA: first academic year. TX: within 2 years |
| `cohort_n` | Students in the starting cohort | CA: `DENOM`, 502C, Overall x Overall, All Programs. TX: prepared n + underprepared n |
| `completed_n` | Students who passed | CA: `VALUE`. TX: prepared completers + underprepared completers |
| `rate` | `completed_n / cohort_n`, 4 decimals | Computed |
| `small_cohort` | 1 if `cohort_n` < 30 | Computed; flagged, never dropped |
| `prepared_n`, `prepared_completed_n` | TX only: students who entered college-ready in math (TSI met or exempt), and those who passed college-level math within 2 years | THECB report 1185 |
| `underprepared_n`, `underprepared_completed_n` | TX only: students who entered not college-ready in math, and those who passed college-level math within 2 years | THECB report 1184 |
| `city`, `county_fips`, `latitude`, `longitude` | Location | IPEDS directory 2023 |
| `sector_label` | IPEDS sector. Some community colleges that award a few bachelor's degrees are "Public, four-year or above" | IPEDS directory 2023 |
| `locale_group` | City, Suburb, Town or Rural | IPEDS `urban_centric_locale`, first digit |
| `ug_enroll_fall2023` | Fall 2023 undergraduate headcount | IPEDS fall enrollment, ftpt=99, degree_seeking=99, class_level=99 |
| `pct_parttime_fall2023` | Share of those undergraduates enrolled part-time | ftpt=2 divided by ftpt=99 |
| `pct_pell_2021_22` | Share of all undergraduates receiving a Pell grant, 2021-22 | IPEDS student financial aid, all undergraduates, `type_of_aid`=5 ("Pell grant"), `percent_of_students` |

## Columns: `atlas_v1_colleges.csv`

Same identifying and federal columns as above, plus:

| Column | Meaning |
|---|---|
| `latest_cohort`, `latest_n`, `latest_rate` | The most recent cohort the state published for that college |
| `pooled_cohorts`, `pooled_n`, `pooled_rate` | The last three cohorts added together; steadier for small colleges |
| `small_cohort` | 1 if `pooled_n` < 30 |

## State measure definitions, in the states' own terms

**California, CCCCO 502C.** Among students in the General Admit Cohort, the proportion who completed transfer-level math in their first academic year of credit enrollment within the district (aligned with the Student Centered Funding Formula). Source: Data Vista Metric Definition Dictionary, read 2026-10-10.

**Texas, THECB C18UC.** First-time summer/fall entering (non-flex entry) degree-seeking undergraduates are tracked to see whether they successfully complete a college-level course in math within 2 years, separately for students who entered college-ready (TSI met or exempt) and not ready. Completion means an A, B or C in a related general education core course. Source: THECB Accountability System, Measures and Definitions, read 2026-10-10.
