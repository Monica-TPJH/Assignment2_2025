import requests
from lxml import html
import csv

URL = "https://www.hko.gov.hk/tc/informtc/historical_tc/fttcw.htm"

resp = requests.get(URL)
resp.raise_for_status()

root = html.fromstring(resp.content)

# Find the table by looking for the header row that contains '年份' and '信號'
# The page has multiple repeated sections; we'll search for the first table that contains '年份' in text
tables = root.xpath('//table')

target_table = None
for t in tables:
    text = ''.join(t.xpath('.//th//text() | .//td//text()'))
    if '年份' in text and '信號' in text:
        target_table = t
        break

if target_table is None:
    raise SystemExit('Could not find target table')

# Extract rows
rows = []
for tr in target_table.xpath('.//tr'):
    cells = [ ' '.join(td.xpath('.//text()')).strip() for td in tr.xpath('.//th | .//td') ]
    if any(cells):
        rows.append(cells)

# The table appears to have a header row followed by data rows. We need to normalize rows where time is split in two columns (hours and minutes)
# From inspection, columns look like: Year, H1 count, H2 count, ... , TotalHours, TotalMinutes
# We'll build CSV with columns: Year, Signal1, Signal2, Signal3, Signal4, Signal5, Signal6, Signal7, TotalHoursDecimal

out_rows = []
for r in rows:
    # skip header-like rows
    if r[0].strip() == '年份' or r[0].strip().startswith('共') or r[0].strip().startswith('平均'):
        continue
    # Some rows may have leading empty cells or extra separators; try to parse numeric year
    try:
        year = int(r[0])
    except ValueError:
        continue
    # Ensure enough columns
    # Many rows have 11 columns: year + 8 signal counts + hours + minutes
    if len(r) >= 11:
        counts = r[1:9]
        hours = r[9]
        minutes = r[10]
    else:
        # skip malformed
        continue
    # convert counts to int
    counts = [int(c) if c.isdigit() or (c and c.replace('−','-').lstrip('-').isdigit()) else 0 for c in counts]
    # convert hours/minutes to total hours as decimal
    try:
        h = int(hours)
        m = int(minutes)
    except ValueError:
        # sometimes minutes are like '05' or with non-ascii; try to extract digits
        import re
        hd = re.sub(r"[^0-9-]","", hours)
        md = re.sub(r"[^0-9]","", minutes)
        h = int(hd) if hd else 0
        m = int(md) if md else 0
    total_hours = h + m/60.0
    out_rows.append([year] + counts + [round(total_hours,2)])

# Write to CSV
csv_path = 'hko_tropical_warnings_1956_2024.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    header = ['Year','Signal1','Signal2','Signal3','Signal4','Signal5','Signal6','Signal7','Signal8','TotalHours']
    writer.writerow(header)
    for r in sorted(out_rows):
        writer.writerow(r)

print('Wrote', csv_path)
