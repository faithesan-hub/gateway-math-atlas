"""Step 2: clean, match and combine the sources into the atlas tables.

Plain-language note: this script takes the raw state and federal files, matches
each state's colleges to their federal ID number (UNITID) using the crosswalk
tables in data/crosswalks/, and writes the combined tables to data/processed/.
You do not need to open it; the codebook (docs/CODEBOOK.md) explains every column.

Run:  python code/02_build.py
"""
import csv
import glob
import gzip
import json
import os

import build_lib as b

SMALL_N = 30  # cohorts below this are flagged as small (author decision point)
CA_METRIC = "502"  # 502C: completed transfer-level math within the district in the first year
CA_YEARS = ["19-20", "20-21", "21-22", "22-23", "23-24"]

FED_COLS = ["city", "county_fips", "latitude", "longitude", "sector_label", "locale_group",
            "ug_enroll_fall2023", "pct_parttime_fall2023", "pct_pell_2021_22"]
LONG_COLS = (["state", "unitid", "ipeds_name", "state_source_id", "state_source_name", "match_level",
              "cohort", "measure_code", "measure_window", "cohort_n", "completed_n", "rate", "small_cohort",
              "prepared_n", "prepared_completed_n", "underprepared_n", "underprepared_completed_n"] + FED_COLS)


def rate(c, n):
    return round(c / n, 4) if n else ""


def build_ca(fed, qa):
    xw = [r for r in b.read_csv(b.XW / "crosswalk_ca.csv") if r["match_level"] == "college"]
    by_dv = {r["dv_id"]: r for r in xw}
    files = sorted(glob.glob(str(b.RAW / "ca" / "college" / "gma_ca_college_*.csv.gz")))
    qa["ca_files_found"] = len(files)
    rows, seen = [], set()
    for path in files:
        dv_id = os.path.basename(path).split("_")[3]
        if dv_id not in by_dv:
            qa.setdefault("ca_files_without_crosswalk", []).append(os.path.basename(path))
            continue
        x = by_dv[dv_id]
        locale_names = set()
        found = {}
        with gzip.open(path, "rt", newline="") as f:
            for r in csv.DictReader(f):
                locale_names.add(r["LOCALE_NAME"])
                if (r["METRIC_ID"] == CA_METRIC and r["DISAGG1_LABEL"] == "Overall" and r["DISAGG2_LABEL"] == "Overall"
                        and r["PROGRAM_NAME"] == "All Programs" and r["SCHOOL_YEAR"] in CA_YEARS):
                    v = r["VALUE"].strip()
                    d = r["DENOM"].strip()
                    n = int(d) if d.isdigit() else None
                    c = int(float(v)) if v and not v.startswith("\\") else None
                    found[r["SCHOOL_YEAR"]] = (n, c)
        if locale_names != {x["dv_name"]}:
            qa.setdefault("ca_locale_name_mismatch", []).append([os.path.basename(path), sorted(locale_names)])
            continue
        seen.add(dv_id)
        rows += ca_rows(x, found, fed, qa)
    # Colleges whose export could not be saved to disk: figures extracted in the browser from the
    # same export file (sha256 recorded per file in data/raw/ca/ca_502C_browser_extract.tsv)
    ext = b.RAW / "ca" / "ca_502C_browser_extract.tsv"
    if ext.exists():
        for r in csv.DictReader(open(ext, newline=""), delimiter="\t"):
            dv_id = r["file"].split("_")[3]
            if dv_id in seen or dv_id not in by_dv:
                continue
            x = by_dv[dv_id]
            if r["locale_name"] != x["dv_name"]:
                qa.setdefault("ca_locale_name_mismatch", []).append([r["file"], r["locale_name"]])
                continue
            found = {}
            for part in list(r.values())[-1].split(";"):
                y, v, d, _ = part.split(",")
                found[y] = (int(d), int(float(v)))
            seen.add(dv_id)
            qa.setdefault("ca_from_browser_extract", []).append(x["dv_name"])
            rows += ca_rows(x, found, fed, qa)
    qa["ca_colleges_in_crosswalk"] = len(xw)
    qa["ca_colleges_with_data"] = len(seen)
    qa["ca_colleges_missing_file"] = sorted(r["dv_name"] for r in xw if r["dv_id"] not in seen)
    return rows


def ca_rows(x, found, fed, qa):
    rows = []
    fd = fed[int(x["unitid"])]
    for y in CA_YEARS:
        n, c = found.get(y, (None, None))
        if n is None:
            qa.setdefault("ca_missing_years", []).append([x["dv_name"], y])
            continue
        rows.append({"state": "CA", "unitid": x["unitid"], "ipeds_name": fd["ipeds_name"],
                     "state_source_id": x["dv_id"], "state_source_name": x["dv_name"], "match_level": "college",
                     "cohort": "20" + y[:2], "measure_code": "CCCCO 502C",
                     "measure_window": "first academic year", "cohort_n": n,
                     "completed_n": c if c is not None else "", "rate": rate(c, n) if c is not None else "",
                     "small_cohort": int(n < SMALL_N), **{k: fd[k] for k in FED_COLS}})
    return rows


def build_tx(fed, qa):
    tx = b.load_tx()
    xw = b.read_csv(b.XW / "crosswalk_tx.csv")
    rows = []
    for x in xw:
        t = tx[x["thecb_inst_id"]]
        fd = fed[int(x["unitid"])]
        for y in ["2020", "2021", "2022"]:
            p = t.get((y, "prepared"))
            u = t.get((y, "underprepared"))
            if p is None and u is None:
                continue
            pn, pc = p or (0, 0)
            un, uc = u or (0, 0)
            n, c = pn + un, pc + uc
            rows.append({"state": "TX", "unitid": x["unitid"], "ipeds_name": fd["ipeds_name"],
                         "state_source_id": x["thecb_inst_id"], "state_source_name": t["name"],
                         "match_level": x["match_level"], "cohort": y, "measure_code": "THECB C18UC (math, prepared + underprepared)",
                         "measure_window": "within 2 years", "cohort_n": n, "completed_n": c, "rate": rate(c, n),
                         "small_cohort": int(n < SMALL_N),
                         "prepared_n": pn if p else "", "prepared_completed_n": pc if p else "",
                         "underprepared_n": un if u else "", "underprepared_completed_n": uc if u else "",
                         **{k: fd[k] for k in FED_COLS}})
    qa["tx_institutions_in_crosswalk"] = len(xw)
    # check: our sum over campus rows equals THECB's own statewide sector total
    used = {x["thecb_inst_id"] for x in xw}
    for y in ["2020", "2021", "2022"]:
        for g in ["prepared", "underprepared"]:
            state_n = tx["390"][(y, g)][0]
            ours = sum(tx[i][(y, g)][0] for i in used if (y, g) in tx[i])
            qa.setdefault("tx_sum_vs_statewide", []).append([y, g, ours, state_n])
    return rows


def main():
    qa = {}
    fed = b.load_federal()
    rows = build_ca(fed, qa) + build_tx(fed, qa)
    b.OUT.mkdir(parents=True, exist_ok=True)
    with open(b.OUT / "atlas_v1_long.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LONG_COLS, extrasaction="ignore")
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r["state"], r["ipeds_name"], r["cohort"])):
            w.writerow(r)
    # one row per college: latest cohort, plus a 3-cohort pooled rate for stability
    latest = {}
    for r in rows:
        latest.setdefault((r["state"], r["unitid"]), []).append(r)
    summary = []
    for (st, u), rs in latest.items():
        rs.sort(key=lambda r: r["cohort"])
        last = rs[-1]
        pool = [r for r in rs[-3:] if r["completed_n"] != ""] or rs[-1:]
        pn = sum(r["cohort_n"] for r in pool if r["completed_n"] != "")
        pc = sum(r["completed_n"] for r in pool if r["completed_n"] != "")
        summary.append({**{k: last[k] for k in ["state", "unitid", "ipeds_name", "state_source_name", "match_level",
                                                "measure_code", "measure_window"] + FED_COLS},
                        "latest_cohort": last["cohort"], "latest_n": last["cohort_n"], "latest_rate": last["rate"],
                        "pooled_cohorts": f"{pool[0]['cohort']}-{pool[-1]['cohort']}", "pooled_n": pn,
                        "pooled_rate": rate(pc, pn), "small_cohort": int(pn < SMALL_N)})
    cols = ["state", "unitid", "ipeds_name", "state_source_name", "match_level", "measure_code", "measure_window",
            "latest_cohort", "latest_n", "latest_rate", "pooled_cohorts", "pooled_n", "pooled_rate", "small_cohort"] + FED_COLS
    with open(b.OUT / "atlas_v1_colleges.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in sorted(summary, key=lambda r: (r["state"], r["ipeds_name"])):
            w.writerow(r)
    qa["rows_long"] = len(rows)
    qa["colleges"] = len(summary)
    json.dump(qa, open(b.OUT / "build_log.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in qa.items() if not isinstance(v, list) or len(v) < 8}, indent=1))


if __name__ == "__main__":
    main()
