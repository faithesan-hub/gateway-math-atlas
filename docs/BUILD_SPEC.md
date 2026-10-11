# Build spec, version 1.0

*Plain-language note: this is the plan the whole build follows. You do not need to edit it, but tell me if any line is wrong.*

```
PROJECT:        US Gateway Mathematics Outcomes Atlas, v1.0
                Archetypes: open dataset (1) + atlas (3) + technical report (9)
QUESTION:       For each public two-year college in the included states, what share of
                new students pass a college-level math course within their first year,
                and how does that relate to federal facts about the college?
SOURCES:        IPEDS Institutional Characteristics + 12-month enrollment (NCES), latest final release
                College Scorecard institution file (US Dept. of Education), latest release
                California Community Colleges Data Vista / Student Success Metrics,
                  transfer-level math in year one (first-time cohort)
                Texas Higher Education Coordinating Board, developmental education
                  accountability measures (college-level math success), by institution
                (vintages, URLs, access dates logged in data/raw/PROVENANCE.txt at fetch)
UNIT:           One college x one cohort year x one state measure
MEASURES:       state_rate        the state's published first-year gateway math rate, as published
                state_cohort_n    denominator where published
                measure_definition  state's own definition, recorded verbatim-paraphrased in codebook
                IPEDS: UNITID, sector, size, % Pell, % part-time, urbanicity
                No cross-state ranking: CA and TX define the measure differently (flagged in report)
OUTPUTS:        data/processed/atlas_v1.csv, crosswalk_ca.csv, crosswalk_tx.csv,
                docs/CODEBOOK.md, data/processed/qa_report.txt, report/stats.json,
                report/figures/*, atlas page (HTML map + lookup), technical report
VENUES:         GitHub release v1.0 -> Zenodo DOI -> atlas page -> technical report on Zenodo
VERIFY POINTS:  (a) each state-to-UNITID match flagged as uncertain
                (b) which CA level to use if results are district-level, not college-level
                (c) which TX measure counts as "gateway math" for the atlas
                (d) five spot-check colleges per state against the state's own website
LICENSE:        Code MIT; data and report CC BY 4.0 with source attribution
ASSUMPTIONS:    CA + TX only; public two-year colleges only; defaults accepted for license.
                Version 2.0 (more states and years) is a separate later release.
```
