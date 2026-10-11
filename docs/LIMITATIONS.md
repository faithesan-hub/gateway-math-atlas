# Limitations

*Plain-language note: what this atlas cannot tell you, and where its data is weak. Read this before using or citing anything. Every credible dataset has a list like this; a short one would be a warning sign.*

1. **California and Texas measure different things, so their numbers must not be compared.** California counts passing transfer-level math within the first year. Texas counts passing a college-level math course within two years. Their cohorts are also defined differently. A Texas rate twice the California rate does not mean Texas colleges do twice as well. The atlas never ranks colleges across states.

2. **These are completion rates, not college quality scores.** Rates reflect who enrolls (preparation, part-time work, family duties, goals) as much as what a college does. Students who never intended to take math, such as some certificate-seekers, are included in the starting cohort in both states.

3. **"Within the district" in California.** A California student counts as passing if they passed at any college in the same district, not only the college they started at. In multi-college districts, a college's rate can include courses taken at a sister college.

4. **Some Texas results are for a whole district or system.** Dallas College, Lone Star College System, San Jacinto College and Tarrant County College report as one unit. Their rates are averages across all their campuses.

5. **Texas colleges do not add up to the Texas statewide total.** The 55 matched Texas institutions account for about 82 to 88 percent of the students in THECB's own statewide community college figure (see `qa_report.txt`, section 3). No public two-year institution with published values was left out. The gap is unexplained in the public documentation and is an open question for THECB. Rates for individual colleges are unaffected.

6. **California colleges add up to slightly more than the California statewide total.** The 115 colleges sum to 2 to 5 percent more students than Data Vista's statewide 502C cohort. The likely reason is that a student who enrolls at two colleges counts in both colleges' cohorts but only once statewide. College rates are as published.

7. **Texas State Technical College, Lamar State Colleges and Lamar Institute of Technology are not included.** The public portal shows no college-level values for them.

8. **California noncredit and special units are excluded.** Eight Data Vista units (six noncredit continuing-education centers, Calbright College, and Los Angeles ITV) have no matching federal record for credit enrollment and are listed as excluded in `crosswalk_ca.csv`.

9. **Small colleges have unstable rates.** Rates for cohorts under 30 students are flagged. The pooled three-cohort rate is steadier and is what the map colors by.

10. **Possible reporting problems are flagged, not fixed.** For example, Weatherford College's 2021 Texas cohort has 12 students against more than 600 in the years around it. The atlas shows the published value and flags it; it does not guess a correction.

11. **The federal facts are from slightly different years.** Enrollment is fall 2023; the Pell share is 2021-22, the most recent year the Education Data Portal provides for that table. These describe the college, not the specific students in each math cohort.

12. **Associations are descriptive.** The relationship between a college's Pell share and its math rate, shown in Figure 2, is a correlation across colleges. It does not show that Pell status causes anything, and it says nothing about individual students.

13. **State data reuse terms.** The California Chancellor's Office and Texas Higher Education Coordinating Board websites carry copyright notices but no explicit reuse license. This atlas republishes only factual counts and rates with full attribution and links, and does not redistribute the states' raw download files; each can be re-downloaded with the steps in the README. The maintainer chose to release on this basis; a confirmation request to each agency is drafted in `docs/AGENCY_EMAIL.md`.
