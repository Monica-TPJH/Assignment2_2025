import pandas as pd
import matplotlib.pyplot as plt

# Read the first 100 rows of the CSV file
df = pd.read_csv('tidal_data.csv', nrows=100)

# Plot bar chart
df['datetime'] = pd.to_datetime(df['datetime'])
plt.figure(figsize=(18, 6))
plt.bar(df['datetime'].dt.strftime('%Y-%m-%d %H:%M'), df['value'])
plt.xlabel('Datetime')
plt.ylabel('Value')
plt.title('Tidal Data - First 100 Entries')
plt.xticks(rotation=90, fontsize=8)
plt.tight_layout()
plt.show()
