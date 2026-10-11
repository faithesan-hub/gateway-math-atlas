"""Step 3: quality checks and the stats file.

Plain-language note: this script counts, compares and flags. It writes
data/processed/qa_report.txt (read it before trusting any number) and
report/stats.json (the ONLY place the report and atlas page take numbers from).

Run:  python code/03_qa.py
"""
import csv
import json
import statistics as st

import build_lib as b

SPOT = {
    "CA": ["Allan Hancock College", "East Los Angeles College", "Mt San Antonio College",
           "Palo Verde College", "Copper Mountain Community College"],
    "TX": ["Alvin Community College", "Tarrant County College District", "Palo Alto College",
           "Clarendon College", "Lone Star College System"],
}


def main():
    long = b.read_csv(b.OUT / "atlas_v1_long.csv")
    cols = b.read_csv(b.OUT / "atlas_v1_colleges.csv")
    log = json.load(open(b.OUT / "build_log.json"))
    L = []
    p = L.append
    p("GATEWAY MATH ATLAS v1.0 - QA REPORT")
    p("Plain-language note: every check below should say OK, or be explained in docs/LIMITATIONS.md.\n")

    # 1. counts
    p("1. ROW COUNTS")
    for s in ["CA", "TX"]:
        p(f"   {s}: {sum(1 for r in long if r['state']==s)} college-cohort rows, "
          f"{sum(1 for r in cols if r['state']==s)} colleges")
    p(f"   CA crosswalk colleges: {log.get('ca_colleges_in_crosswalk')}  with data: {log.get('ca_colleges_with_data')}")
    if log.get("ca_colleges_missing_file"):
        p(f"   CA colleges without a data file: {len(log['ca_colleges_missing_file'])} -> {log['ca_colleges_missing_file']}")
    for k in ["ca_locale_name_mismatch", "ca_files_without_crosswalk", "ca_missing_years"]:
        if log.get(k):
            p(f"   FLAG {k}: {log[k]}")
    p(f"   TX institutions in crosswalk: {log.get('tx_institutions_in_crosswalk')}")

    # 2. matching
    p("\n2. MATCH TO FEDERAL IDS")
    xca = b.read_csv(b.XW / "crosswalk_ca.csv")
    xtx = b.read_csv(b.XW / "crosswalk_tx.csv")
    p(f"   CA: {sum(r['match_level']=='college' for r in xca)} of {len(xca)} Data Vista colleges matched; "
      f"{sum(r['match_level']=='excluded' for r in xca)} excluded (noncredit/online/TV units, listed in crosswalk)")
    p(f"   TX: {len(xtx)} institutions matched; district-level matches: "
      f"{[r['ipeds_name'] for r in xtx if r['match_level']=='district']}")
    dup = [u for u in {r['unitid'] for r in cols} if sum(1 for c in cols if c['unitid'] == u) > 1]
    p(f"   Duplicate UNITIDs in college table: {dup or 'none - OK'}")

    # 3. range checks
    p("\n3. RANGE CHECKS")
    bad = [r for r in long if r["rate"] != "" and not (0 <= float(r["rate"]) <= 1)]
    p(f"   Rates outside 0-1: {len(bad) or 'none - OK'}")
    bad = [r for r in long if r["completed_n"] != "" and int(r["completed_n"]) > int(r["cohort_n"])]
    p(f"   Completers > cohort: {len(bad) or 'none - OK'}")
    small = [f"{r['ipeds_name']} {r['cohort']} (n={r['cohort_n']})" for r in long if r["small_cohort"] == "1"]
    p(f"   Small cohorts (n<30), flagged not dropped: {len(small)} -> {small}")
    jumps = []
    by = {}
    for r in long:
        by.setdefault((r["state"], r["unitid"]), []).append(r)
    for k, rs in by.items():
        rs.sort(key=lambda r: r["cohort"])
        for a, c in zip(rs, rs[1:]):
            na, nc = int(a["cohort_n"]), int(c["cohort_n"])
            if min(na, nc) > 0 and (max(na, nc) / min(na, nc) > 3):
                jumps.append(f"{c['ipeds_name']} {a['cohort']}->{c['cohort']} n {na}->{nc}")
    p(f"   Cohort size jumps >3x year to year (possible reporting issue): {jumps or 'none - OK'}")
    p("   CA check, sum of matched colleges vs Data Vista statewide 502C (cohort n / completers):")
    import gzip
    sw = {}
    with gzip.open(b.RAW / "ca" / "gma_ca_Statewide_20261010T230831.csv.gz", "rt", newline="") as f:
        for r in csv.DictReader(f):
            if (r["METRIC_ID"] == "502" and r["DISAGG1_LABEL"] == "Overall" and r["DISAGG2_LABEL"] == "Overall"
                    and r["PROGRAM_NAME"] == "All Programs"):
                sw["20" + r["SCHOOL_YEAR"][:2]] = (int(r["DENOM"]), int(float(r["VALUE"])))
    for y in sorted(sw):
        rs = [r for r in long if r["state"] == "CA" and r["cohort"] == y]
        on, oc = sum(int(r["cohort_n"]) for r in rs), sum(int(r["completed_n"]) for r in rs if r["completed_n"] != "")
        p(f"      {y}  ours {on:>7} / {oc:>6}   statewide {sw[y][0]:>7} / {sw[y][1]:>6}   ratio n {on/sw[y][0]:.3f}")
    p("      NOTE: colleges sum to 2-5% MORE than the statewide count. Likely cause: a student enrolled at two colleges counts in both college cohorts but once statewide. Not confirmed by CCCCO; see LIMITATIONS.md.")
    p("   TX check, sum of matched institutions vs THECB statewide community-college total (n):")
    for y, g, ours, state in log.get("tx_sum_vs_statewide", []):
        p(f"      {y} {g:13s} ours {ours:>6}  THECB statewide {state:>6}  ratio {ours/state:.3f}")
    p("      NOTE: ratio below 1 means THECB's statewide figure counts students not attributed to any listed college.")
    p("      All public two-year colleges were queried; Lamar State Colleges, Lamar Institute and TSTC return no")
    p("      college-level values in the public portal. Open question for THECB, see LIMITATIONS.md.")

    # 4. spot checks
    p("\n4. SPOT CHECKS (author verifies these by hand against the state website)")
    for s, names in SPOT.items():
        for n in names:
            rs = [r for r in long if r["state"] == s and r["ipeds_name"] == n]
            for r in rs:
                extra = ""
                if s == "TX":
                    extra = (f"  [prepared {r['prepared_completed_n']}/{r['prepared_n']}, "
                             f"underprepared {r['underprepared_completed_n']}/{r['underprepared_n']}]")
                p(f"   {s} | {n} | source name '{r['state_source_name']}' | cohort {r['cohort']} | "
                  f"{r['completed_n']} of {r['cohort_n']} = {float(r['rate'])*100:.1f}%{extra}")
            if not rs:
                p(f"   {s} | {n} | NOT FOUND - check")

    # stats file
    stats = {"version": "1.0", "built_from": "data/processed/atlas_v1_colleges.csv"}
    for s in ["CA", "TX"]:
        cs = [c for c in cols if c["state"] == s and c["latest_rate"] != ""]
        big = [c for c in cs if c["small_cohort"] == "0"]
        rates = sorted(float(c["latest_rate"]) for c in big)
        latest = max(c["latest_cohort"] for c in cs) if cs else ""
        lr = [r for r in long if r["state"] == s and r["cohort"] == latest and r["completed_n"] != ""]
        stats[s] = {
            "colleges": len(cs),
            "colleges_not_small": len(big),
            "latest_cohort": latest,
            "students_latest_cohort": sum(int(r["cohort_n"]) for r in lr),
            "completers_latest_cohort": sum(int(r["completed_n"]) for r in lr),
            "pooled_rate_latest_cohort": round(sum(int(r["completed_n"]) for r in lr) / sum(int(r["cohort_n"]) for r in lr), 4) if lr else None,
            "median_college_rate": round(st.median(rates), 4) if rates else None,
            "p10_college_rate": round(rates[int(0.1 * (len(rates) - 1))], 4) if rates else None,
            "p90_college_rate": round(rates[int(0.9 * (len(rates) - 1))], 4) if rates else None,
            "min_college": min(big, key=lambda c: float(c["latest_rate"]))["ipeds_name"] if big else None,
            "min_rate": min(rates) if rates else None,
            "max_college": max(big, key=lambda c: float(c["latest_rate"]))["ipeds_name"] if big else None,
            "max_rate": max(rates) if rates else None,
        }
        # simple association with Pell share (descriptive only)
        pairs = [(float(c["pct_pell_2021_22"]), float(c["latest_rate"])) for c in big if c["pct_pell_2021_22"] not in ("", None)]
        if len(pairs) > 5:
            stats[s]["pearson_r_rate_vs_pell"] = round(st.correlation([a for a, _ in pairs], [b_ for _, b_ in pairs]), 3)
            stats[s]["n_pell_pairs"] = len(pairs)
    json.dump(stats, open(b.ROOT / "report" / "stats.json", "w"), indent=1)
    p("\n5. HEADLINE NUMBERS (written to report/stats.json)")
    p(json.dumps(stats, indent=1))
    open(b.OUT / "qa_report.txt", "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
