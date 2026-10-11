"""Shared helpers for the Gateway Math Atlas build.

Plain-language note: this file holds small reusable pieces (reading the raw
files, building the federal facts table). You do not need to open it.
"""
import csv
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
XW = ROOT / "data" / "crosswalks"
OUT = ROOT / "data" / "processed"

# Urban Institute Education Data Portal code lists (checked via /api/v1/api-values/ on 2026-10-10)
PELL_TYPE_OF_AID = 5          # "5 - Pell grant"
FTPT_TOTAL, FTPT_PART = 99, 2  # "99 - Total", "2 - Part-time"
SECTOR_LABEL = {0: "Administrative unit", 1: "Public, four-year or above",
                4: "Public, two-year", 7: "Public, less-than two-year"}
LOCALE_GROUP = {1: "City", 2: "Suburb", 3: "Town", 4: "Rural"}


def load_federal():
    """Return {unitid: dict of federal facts} for CA and TX public institutions."""
    pages = json.load(open(RAW / "federal" / "gma_ipeds_urban_2023_CA_TX.json"))
    directory, enr_total, enr_part, pell = {}, {}, {}, {}
    for p in pages:
        url = p["url"]
        for r in p["body"]["results"]:
            u = r["unitid"]
            if "/directory/" in url:
                directory[u] = r
            elif "/fall-enrollment/" in url:
                if r.get("degree_seeking") == 99 and r.get("class_level") == 99 and r.get("level_of_study") == 1:
                    if r["ftpt"] == FTPT_TOTAL:
                        enr_total[u] = r["enrollment_fall"]
                    elif r["ftpt"] == FTPT_PART:
                        enr_part[u] = r["enrollment_fall"]
            elif "/sfa-all-undergraduates/" in url:
                if r["type_of_aid"] == PELL_TYPE_OF_AID and r.get("ftpt") == 99 and r.get("level_of_study") == 1:
                    pell[u] = r["percent_of_students"]
    fed = {}
    for u, d in directory.items():
        tot = enr_total.get(u)
        part = enr_part.get(u)
        loc = d.get("urban_centric_locale")
        fed[u] = {
            "unitid": u,
            "ipeds_name": d["inst_name"],
            "state": d["state_abbr"],
            "city": d["city"],
            "county_fips": d["county_fips"],
            "latitude": d["latitude"],
            "longitude": d["longitude"],
            "sector": d["sector"],
            "sector_label": SECTOR_LABEL.get(d["sector"], str(d["sector"])),
            "locale_group": LOCALE_GROUP.get(loc // 10 if isinstance(loc, int) and loc > 0 else None, ""),
            "ug_enroll_fall2023": tot if (tot is not None and tot >= 0) else "",
            "pct_parttime_fall2023": round(part / tot, 4) if (tot and part is not None and part >= 0 and tot > 0) else "",
            "pct_pell_2021_22": pell.get(u, "") if (pell.get(u) is not None and pell.get(u, -1) >= 0) else "",
        }
    return fed


def load_tx():
    """Texas C18UC math rows -> {thecb_inst_id: {(cohort, group): (n, completed)}}."""
    d = json.load(open(RAW / "tx" / "gma_tx_thecb_c18uc_raw.json"))
    years = ["2020", "2021", "2022"]
    num = lambda s: None if not str(s).replace(",", "").strip() else int(str(s).replace(",", "").strip())
    out = {}
    for iid, name, rep, rows in d["math_rows"]:
        total, comp = rows[0], rows[1]
        group = {1184: "underprepared", 1185: "prepared"}[int(rep)]
        for k, y in enumerate(years):
            n, c = num(total[2 + 2 * k]), num(comp[2 + 2 * k])
            if n is None:
                continue
            out.setdefault(str(iid), {"name": name})[(y, group)] = (n, c or 0)
    return out


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
