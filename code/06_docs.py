"""Step 6: write the headline numbers into README.md from report/stats.json.

Plain-language note: this keeps the README's numbers identical to the data.
Nobody types a number into the README by hand.
"""
import json
import re

import build_lib as b

s = json.load(open(b.ROOT / "report" / "stats.json"))
p = lambda v: f"{v*100:.1f}%"
lines = []
for st, name, win in [("CA", "California", "transfer-level math in their first year"), ("TX", "Texas", "a college-level math course within two years")]:
    x = s[st]
    lines.append(
        f"- **{name}:** {x['colleges']} colleges. Across the {x['latest_cohort']} cohort, "
        f"{x['completers_latest_cohort']:,} of {x['students_latest_cohort']:,} students "
        f"({p(x['pooled_rate_latest_cohort'])}) passed {win}. "
        f"The middle college's rate was {p(x['median_college_rate'])}; one in ten colleges was below "
        f"{p(x['p10_college_rate'])} and one in ten above {p(x['p90_college_rate'])}.")
block = "\n".join(lines) + "\n\nNumbers come from `report/stats.json`, written by `code/03_qa.py`."
readme = (b.ROOT / "README.md").read_text()
readme = re.sub(r"<!--STATS-->.*?(?=\n## )|<!--STATS-->", "<!--STATS-->\n" + block + "\n", readme, count=1, flags=re.S)
(b.ROOT / "README.md").write_text(readme)
print(block)
