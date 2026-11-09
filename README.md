# Board Cyber Risk Dashboard

Turns a CSV of key risk indicators (KRIs) into a clean, single-page HTML dashboard that a board or executive committee can read in a minute.

Boards do not need 40 charts. They need to know what is on target, what needs watching, what needs action, and whether things are getting better. This tool answers those four questions.

## Quick start

```bash
python build_dashboard.py kri_data.csv dashboard.html
```

Open `dashboard.html` in any browser. No dependencies beyond Python 3, and no internet connection is needed to view the result.

## What the dashboard shows

For each indicator:

- The latest value and its unit
- A status label: **On target**, **Watch** or **Action needed** (shown as text as well as colour)
- A small trend line across the reporting periods
- The target and whether the indicator is improving or worsening

A summary line at the top counts how many indicators fall in each status.

## Input format

| Column | Meaning |
|---|---|
| `kri` | Indicator name |
| `unit` | `count`, `%`, `hours` and so on |
| `higher_is_worse` | `yes` if a higher number is bad (open vulnerabilities), `no` if lower is bad (patch compliance) |
| `target` | Value at or better than this is on target |
| `red` | Value worse than this needs action |
| Remaining columns | One column per reporting period, oldest first |

Add or remove rows and periods freely. The script reads the period columns automatically.

## Sample indicators

The sample file uses fictional data for eight common KRIs:

- Critical vulnerabilities open over 30 days
- Patch compliance
- Phishing simulation click rate
- MFA coverage on privileged accounts
- Mean time to detect and mean time to respond
- Vendors with overdue security assessments
- Backup restore tests passed

## Choosing good KRIs

- Pick indicators the board can act on, not technical noise.
- Set targets with the risk owner and agree them in advance.
- Keep the list short. Six to ten indicators is enough.
- Explain any red status in a sentence: what happened and what is being done.

## Limitations

- This is an illustrative generator. Targets and thresholds in the sample are examples, not benchmarks.
- It shows indicator status. It does not replace the narrative and risk discussion a board paper needs.

## Author

E.O. Acheampong. GRC, risk and cybersecurity compliance.
