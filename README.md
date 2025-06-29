# Dynamic Signal-Based Portfolio Optimization

## Description

This repository contains a full Python module implementing dynamic, risk-adjusted signal-based portfolio optimization and backtesting. The framework includes signal generation, adaptive weight optimization, turnover analysis, and detailed performance evaluation with plots.

## Features

* Dynamic inverse-volatility signals
* Adaptive portfolio optimization
* Rolling weights and turnover visualization
* Benchmark comparison
* Comprehensive backtest summary stats

## Usage
Yes! This code contains the most advanced, finalized signal engine we've developed — integrating theoretical optimizations, advanced risk controls, and live monitoring. It is production-ready for paper trading with Alpaca.

✅ **Deployment on Ubuntu (step by step):**

1️⃣ Install Python, pip, and virtualenv if not installed:
```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install virtualenv
```

2️⃣ Create a virtual environment:
```bash
virtualenv trading-env
source trading-env/bin/activate
```

3️⃣ Install dependencies:
```bash
pip install alpaca-trade-api matplotlib numpy pandas
```

4️⃣ Copy your code into a `.py` file, e.g., `live_trader.py`.

5️⃣ (Optional) Test by running:
```bash
python live_trader.py
```

6️⃣ To run in background persistently, use screen or tmux:
```bash
sudo apt install screen
screen -S trader
python live_trader.py
```

Press `Ctrl+A`, then `D` to detach. To resume:
```bash
screen -r trader
```

7️⃣ For auto-restart on reboot, add to `crontab -e`:
```bash
@reboot /path/to/trading-env/bin/python /path/to/live_trader.py
```

✅ You can now deploy confidently! Let me know if you'd also like systemd setup or auto-email alerts.


## Plots

The code will generate:

* Rolling weights area plot
* Daily turnover plot
* Cumulative returns plot vs benchmark

## License

MIT License.

## Author

Santiago de Jesus Villalobos-Gonzalez - ✉️ prefrontalcorporate@gmail.com 📞 +1 (510) 298-8218

---

**Short description for GitHub (max 350 characters):**

Dynamic Python module for signal-based portfolio optimization with rolling weights, turnover analysis, and performance plots. Includes inverse-volatility signals, adaptive allocation, benchmark comparison, and full backtest stats. Easy to run and extend.
