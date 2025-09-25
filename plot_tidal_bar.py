import os
import glob
import pandas as pd
import matplotlib.pyplot as plt


def find_input_file():
	# prefer these names if present
	candidates = ['tidal_data.csv', 'tides.csv', 'hko_tropical_warnings_1956_2024.csv']
	for c in candidates:
		if os.path.exists(c):
			return c
	# fallback: any csv in the folder
	csvs = glob.glob('*.csv')
	if csvs:
		return csvs[0]
	return None


infile = find_input_file()
if infile is None:
	raise SystemExit("No CSV file found. Please add 'tidal_data.csv' or 'tides.csv' to the project folder.")

print(f"Using input file: {infile}")

# Try reading
df = pd.read_csv(infile, nrows=100)

# Try to find datetime and value columns
datetime_col = None
value_col = None
for col in df.columns:
	lname = col.lower()
	if 'date' in lname or 'time' in lname:
		datetime_col = col
	if value_col is None and (('value' in lname) or ('height' in lname) or ('level' in lname) or df[col].dtype.kind in 'fi'):
		# pick numeric as value candidate
		if df[col].dtype.kind in 'fi' and 'year' not in lname and 'hour' not in lname:
			value_col = col

if datetime_col is None:
	# try first column
	datetime_col = df.columns[0]

if value_col is None:
	# try second column
	if len(df.columns) > 1:
		value_col = df.columns[1]
	else:
		raise SystemExit('Could not find a numeric value column in the CSV')

# parse datetime
try:
	df[datetime_col] = pd.to_datetime(df[datetime_col])
except Exception:
	# if parsing fails, create a simple index
	df[datetime_col] = pd.date_range(start='2000-01-01', periods=len(df), freq='H')

# plotting
plt.figure(figsize=(14, 5))
labels = df[datetime_col].dt.strftime('%Y-%m-%d %H:%M')
plt.bar(labels, df[value_col])
plt.xlabel('Datetime')
plt.ylabel(value_col)
plt.title(f'Tidal Data - First {len(df)} Entries (from {os.path.basename(infile)})')
plt.xticks(rotation=90, fontsize=7)
plt.tight_layout()

# save to file so script can run headless
out_png = 'plot_tidal_bar.png'
plt.savefig(out_png, dpi=200)
print(f'Saved plot to {out_png}')

try:
	plt.show()
except Exception:
	pass
