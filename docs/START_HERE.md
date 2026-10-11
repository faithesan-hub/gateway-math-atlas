# Start Here: US Gateway Mathematics Outcomes Atlas

*Read this first. It explains your project in plain language. Words in bold are explained in [GLOSSARY.md](GLOSSARY.md).*

**Status: version 1.0 verified and released on GitHub. Zenodo DOI next.**

## What you are building

A free online lookup where anyone can find a US college and see how many of its new students pass their first college-level math class, alongside basic federal facts about that college.

## Why it matters

The first college-level math class (the **gateway math course**) is where many students stall. Students who do not pass it in their first year are much less likely to finish any degree. Many states now report how each college does on this, but every state publishes it differently, on a different website, with different college codes. The federal government knows a lot about every college, but it does not track this math result at all.

So today, a researcher or policymaker who wants to compare colleges across states has to hunt through each state's website by hand and match colleges one at a time. This project does that matching once, carefully, and publishes the result so nobody has to repeat it.

Think of it like a single airline arrivals board for a whole country, where each airport used to post its own board in its own format.

## Where the information comes from

All sources are free and public.

| Source | In plain terms | What one row looks like | Link |
|---|---|---|---|
| IPEDS (federal) | The US Department of Education's yearly record of every college that takes federal aid | One college: name, state, ID number, type, size, share of students with Pell Grants | https://nces.ed.gov/ipeds/ |
| College Scorecard (federal) | The Department's public file with extra facts like completion and earnings | One college: ID number, graduation rate, median debt | https://collegescorecard.ed.gov/data/ |
| California Community Colleges, Data Vista / Student Success Metrics (state) | California's public report of how many first-time students pass transfer-level math in year one | One college or district, one starting year, one student group: the percent who passed | https://datavista.cccco.edu/ |
| Texas Higher Education Coordinating Board, accountability reports (state) | Texas's public report on developmental students reaching college-level math | One college, one year: the percent who succeeded | https://www.highered.texas.gov/ |
| Other states (to confirm) | Further state reports, added where they publish college-by-college math results | Varies by state | Listed in the build spec |

## What you will have at the end of version 1.0

- [x] **A public project page** on GitHub where anyone can see and reuse your work: https://github.com/faithesan-hub/gateway-math-atlas
- [ ] **A permanent citation number (DOI)** from Zenodo, so others can cite version 1.0: next step, after GitHub
- [x] **The joined dataset**: one table, every included college, its state math result, and its federal facts, with a codebook
- [x] **The online atlas**: a browsable map and lookup page
- [ ] **A short technical report** describing how it was built and what it shows
- [x] **The college ID crosswalk** for each state, published so others can reuse the matching

Version 2.0 is a later release that adds states and years. It gets its own DOI under the same project.

## How it connects to your work

Faith Oluwafunmitan Esan is the principal investigator and maintainer of the atlas, as an independent researcher. Version 2.0 extends it to more states and newer years.

## What you need to do

| Your task | When | Time |
|---|---|---|
| Create accounts (ORCID, GitHub, Zenodo) | Now | 15 min |
| Answer five setup questions | Now | 10 min |
| Help get the state data files (see note) | Early in the build | 15 to 30 min |
| Check the results using the checklist | When the draft is ready | 1 to 2 hours |
| Approve publishing | After checking | 5 min |

Everything else is built for you.

## The steps ahead

1. **Data collected.** We download the public sources and record exactly where each came from.
2. **Colleges matched.** We connect each state's college codes to the federal ID numbers.
3. **Data combined and checked.** One table, with counts and spot checks you can confirm by hand.
4. **First map and chart.** You see the atlas for the first time.
5. **Draft report and atlas page.** Every number comes straight from the data.
6. **Ready for your check.** You verify, then we publish version 1.0.

*You are here: published. Next, the Zenodo DOI.*
