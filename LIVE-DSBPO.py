import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

API_KEY = 'PKJLU07U4RXCV69HX10D'
SECRET_KEY = 'z4LsjCVgauHG5jfCZ5Nid28jsPN1w4qPhjVi4nS6'
BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

assets = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN']

weights = np.array([0.20, 0.20, 0.20, 0.20, 0.20])

portfolio_value = float(api.get_account().cash)

allocations = {symbol: (portfolio_value * weight) for symbol, weight in zip(assets, weights)}

for symbol, allocation in allocations.items():
    latest_price = float(api.get_latest_trade(symbol).price)
    qty = allocation / latest_price
    api.submit_order(symbol=symbol, qty=qty, side='buy', type='market', time_in_force='day')

print("Orders submitted!")

prices = {s: [] for s in assets}
risk_metrics = []

for _ in range(100):  # simulate 100 monitoring cycles
    for symbol in assets:
        price = float(api.get_latest_trade(symbol).price)
        prices[symbol].append(price)

    pnl = sum([(prices[s][-1] - prices[s][0]) / prices[s][0] for s in assets]) / len(assets)
    volatility = np.std([np.std(np.diff(prices[s])) for s in assets])
    sharpe = pnl / volatility if volatility > 0 else 0

    risk_metrics.append((pnl, volatility, sharpe))

    if sharpe < 0.5:
        print(f"[ALERT] Low Sharpe detected: {sharpe:.2f}")

    plt.figure(figsize=(10, 6))
    for s in assets:
        plt.plot(prices[s], label=s)
    plt.title("Live Price Monitoring")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.pause(1)
    plt.clf()

    time.sleep(60)

plt.close()

print("Monitoring finished.")
