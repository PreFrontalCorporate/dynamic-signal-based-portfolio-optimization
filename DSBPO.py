import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Simulate returns data ---
np.random.seed(42)
dates = pd.date_range("2020-01-01", periods=500, freq='D')
assets = ["Asset 1", "Asset 2", "Asset 3", "Asset 4", "Asset 5"]
returns = pd.DataFrame(0.0005 + 0.01 * np.random.randn(len(dates), len(assets)), index=dates, columns=assets)

# --- Signal generator ---
def generate_signals(window_returns, alpha=0.2):
    vol = window_returns.std().values
    signals = 1 / (vol + 1e-6)  # inverse volatility signal
    signals /= np.sum(signals)   # normalize to sum to 1
    signals = np.clip(signals, 0, 1)  # ensure in [0, 1]
    return signals

# --- Portfolio optimizer ---
def optimize_portfolio(expected_returns, signals):
    active_assets = signals > 0.05  # threshold for active
    if not np.any(active_assets):
        return np.ones_like(signals) / len(signals)
    weights = np.zeros_like(signals, dtype=float)
    weights[active_assets] = expected_returns[active_assets] * signals[active_assets]
    if np.sum(weights) == 0:
        weights[active_assets] = 1.0
    weights /= np.sum(weights)
    return weights

# --- Initialize ---
lookback = 60
weights_list = []
turnover_list = []
cum_returns = [0]
prev_weights = np.ones(len(assets)) / len(assets)

# --- Backtest loop ---
for t in range(lookback, len(returns)):
    window = returns.iloc[t-lookback:t]
    expected_ret = window.mean().values
    signals = generate_signals(window)
    
    new_weights = optimize_portfolio(expected_ret, signals)
    turnover = np.sum(np.abs(new_weights - prev_weights))
    
    daily_ret = np.dot(returns.iloc[t], new_weights)
    cum_returns.append(cum_returns[-1] + daily_ret)
    
    weights_list.append(new_weights)
    turnover_list.append(turnover)
    prev_weights = new_weights

# --- Build DataFrames for plotting ---
weights_df = pd.DataFrame(weights_list, index=returns.index[lookback:], columns=assets)
cum_returns = np.array(cum_returns[1:])
cum_returns = np.cumprod(1 + cum_returns) - 1

# Equal-weight benchmark
benchmark_cum = np.cumprod(1 + returns.iloc[lookback:].mean(axis=1)) - 1

# --- Calculate summary statistics ---
total_return = cum_returns[-1]
annualized_return = (1 + total_return) ** (252 / len(cum_returns)) - 1
annualized_vol = np.std(np.diff(cum_returns)) * np.sqrt(252)
sharpe_ratio = annualized_return / (annualized_vol + 1e-6)
avg_turnover = np.mean(turnover_list)

# --- Plot ---
fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# Weights plot
weights_df.plot.area(ax=axs[0], title="Rolling Portfolio Weights (Dynamic Signals)")
axs[0].set_ylabel("Weight")
axs[0].legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

# Turnover plot
axs[1].plot(weights_df.index, turnover_list, color='brown')
axs[1].set_title("Daily Portfolio Turnover")
axs[1].set_ylabel("Turnover")

# Cumulative returns plot
axs[2].plot(weights_df.index, cum_returns, label="Optimized Portfolio (Net of Costs)", color='blue')
axs[2].plot(weights_df.index, benchmark_cum, label="Equal-Weight Benchmark", color='gray', linestyle='--')
axs[2].set_title("Backtested Portfolio Performance (Dynamic Signals)")
axs[2].set_ylabel("Cumulative Return")
axs[2].legend()

plt.xlabel("Days")
plt.tight_layout()
plt.show()

# --- Print summary ---
print("--- Backtest Summary ---")
print(f"Total Return: {total_return * 100:.2f}%")
print(f"Annualized Return: {annualized_return * 100:.2f}%")
print(f"Annualized Volatility: {annualized_vol * 100:.2f}%")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
print(f"Average Daily Turnover: {avg_turnover * 100:.2f}%")
