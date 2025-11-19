import pandas as pd
import numpy as np
from scipy import signal
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from datetime import datetime

# Load data
df = pd.read_csv('/Users/stephencornelius/Projects/product-copilot/data/bitcoin-daily-price-2025.csv')

# Clean price data - remove $ and commas, drop rows with missing prices
df['Price'] = df['Price'].str.replace('$', '').str.replace(',', '')
df = df[df['Price'].notna() & (df['Price'] != '')]
df['Price'] = df['Price'].astype(float)
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df = df.sort_values('Date').reset_index(drop=True)

print("=== Bitcoin Price Analysis (2025 Data) ===\n")
print(f"Data range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
print(f"Total days: {len(df)}")
print(f"Price range: ${df['Price'].min():,.2f} - ${df['Price'].max():,.2f}\n")

# Calculate daily returns
df['Daily_Return'] = df['Price'].pct_change() * 100
df['Price_Change'] = df['Price'].diff()

# Identify dips using different methods
print("=== Defining 'Dips' ===\n")

# Method 1: Percentage drops from previous day
threshold_pct = 2.0
df['Drop_2pct'] = df['Daily_Return'] < -threshold_pct
dips_2pct = df[df['Drop_2pct']]
print(f"Method 1 - Days with >2% drop from previous day: {len(dips_2pct)}")
print(f"  Frequency: ~{len(dips_2pct) / (len(df) / 30):.1f} per month")

# Method 2: Standard deviation from rolling mean
window = 14  # 2 weeks
df['Rolling_Mean'] = df['Price'].rolling(window=window).mean()
df['Rolling_Std'] = df['Price'].rolling(window=window).std()
df['Z_Score'] = (df['Price'] - df['Rolling_Mean']) / df['Rolling_Std']
df['Dip_StdDev'] = df['Z_Score'] < -1.0
dips_stddev = df[df['Dip_StdDev']].dropna()
print(f"Method 2 - Days >1 std dev below 14-day mean: {len(dips_stddev)}")
print(f"  Frequency: ~{len(dips_stddev) / (len(df) / 30):.1f} per month")

# Method 3: Local minima
peaks, properties = signal.find_peaks(-df['Price'].values, distance=5, prominence=1000)
local_minima = df.iloc[peaks]
print(f"Method 3 - Local minima (5-day spacing): {len(local_minima)}")
print(f"  Frequency: ~{len(local_minima) / (len(df) / 30):.1f} per month\n")

# Test for periodicity
print("=== Testing for Periodic Patterns ===\n")

# Autocorrelation
from pandas.plotting import autocorrelation_plot
autocorr_values = [df['Price'].autocorr(lag=i) for i in range(1, 31)]
max_autocorr = max(autocorr_values)
best_lag = autocorr_values.index(max_autocorr) + 1
print(f"Autocorrelation analysis:")
print(f"  Strongest correlation at {best_lag}-day lag: {max_autocorr:.3f}")
if max_autocorr > 0.5:
    print(f"  This suggests a {best_lag}-day cycle might exist")
else:
    print(f"  Weak autocorrelation suggests no clear periodic pattern")

# Fourier analysis for dominant frequencies
from scipy.fft import fft, fftfreq
prices_detrended = df['Price'] - df['Price'].rolling(window=7).mean()
prices_detrended = prices_detrended.dropna()
yf = fft(prices_detrended.values)
xf = fftfreq(len(prices_detrended), 1)
power = np.abs(yf)**2
positive_freqs = xf[:len(xf)//2]
positive_power = power[:len(power)//2]
if len(positive_freqs) > 1 and positive_freqs[1] > 0:
    dominant_freq_idx = np.argmax(positive_power[1:]) + 1
    dominant_period = 1 / positive_freqs[dominant_freq_idx] if positive_freqs[dominant_freq_idx] > 0 else 0
    print(f"  Fourier analysis dominant period: ~{dominant_period:.1f} days\n")

# Historical success rate
print("=== Historical Success Rate of Buying at Dips ===\n")

def analyze_buy_strategy(buy_dates, df, hold_days=[7, 14, 30]):
    results = {}
    for days in hold_days:
        gains = []
        for idx in buy_dates.index:
            buy_price = df.loc[idx, 'Price']
            future_idx = idx + days
            if future_idx < len(df):
                sell_price = df.iloc[future_idx]['Price']
                gain_pct = ((sell_price - buy_price) / buy_price) * 100
                gains.append(gain_pct)
        
        if gains:
            results[days] = {
                'mean': np.mean(gains),
                'median': np.median(gains),
                'positive': sum(1 for g in gains if g > 0) / len(gains) * 100
            }
    return results

# Analyze Method 2 (std dev dips)
if len(dips_stddev) > 0:
    results_dip = analyze_buy_strategy(dips_stddev, df)
    print("Buying at dips (>1 std dev below mean):")
    for days, metrics in results_dip.items():
        print(f"  {days}-day hold: Mean {metrics['mean']:+.2f}%, Median {metrics['median']:+.2f}%, {metrics['positive']:.0f}% profitable")

# Compare to random buying
random_samples = df.sample(n=min(len(dips_stddev), len(df)-30), random_state=42)
results_random = analyze_buy_strategy(random_samples, df)
print("\nBuying on random days (baseline):")
for days, metrics in results_random.items():
    print(f"  {days}-day hold: Mean {metrics['mean']:+.2f}%, Median {metrics['median']:+.2f}%, {metrics['positive']:.0f}% profitable")

# DCA comparison
daily_returns_mean = df['Daily_Return'].mean()
print(f"\nDaily price change (DCA proxy): Mean {daily_returns_mean:+.3f}% per day")
print(f"  7-day equivalent: {daily_returns_mean * 7:+.2f}%")
print(f"  14-day equivalent: {daily_returns_mean * 14:+.2f}%")
print(f"  30-day equivalent: {daily_returns_mean * 30:+.2f}%")

print("\n=== Summary Statistics ===")
print(f"Average daily volatility: {df['Daily_Return'].std():.2f}%")
print(f"Largest single-day drop: {df['Daily_Return'].min():.2f}%")
print(f"Largest single-day gain: {df['Daily_Return'].max():.2f}%")
print(f"Overall return (first to last day): {((df['Price'].iloc[-1] - df['Price'].iloc[0]) / df['Price'].iloc[0] * 100):+.2f}%")
