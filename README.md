# High-Performance Quantitative Trading & Multi-Indicator Optimization System

A high-throughput quantitative trading backtesting framework and automated live execution engine built in Python. The system features multi-indicator signal filtration, Numba JIT-accelerated vector computation, Optuna Bayesian hyperparameter optimization, and exchange connectivity via CCXT.

---

## System Architecture

The architecture is divided into three functional layers:

1. **JIT-Accelerated Backtesting Core (`parameter_training.py`)**:
   - Compiles core iteration logic down to native machine instructions using Numba (`@njit`).
   - Achieves orders-of-magnitude speedups over pure-Python backtesting loops, evaluating thousands of historical bars within milliseconds.
   - Interfaces with Optuna for automated Bayesian optimization across multidimensional parameter spaces.

2. **Signal Filtration & Strategy Execution (`main_funcion.py`)**:
   - Multi-indicator statistical validation combining trend strength, market efficiency, volatility expansion, and volume anomalies.
   - Enforces strict risk-managed position transitions.

3. **Live Market Connectivity (CCXT Integration)**:
   - Interfaces directly with cryptocurrency exchange endpoints (e.g., Binance, Bybit) for real-time order placement, position tracking, and balance synchronization.

---

## Strategy & Technical Indicators

The signal generator evaluates market regimes using a synchronized indicator stack:

- **Kaufman's Efficiency Ratio (ER)**: Quantifies market trend efficiency versus noise, avoiding whipsaw trades in range-bound chop.
- **Linear Regression ($R^2$) Determination**: Confirms the statistical linearity and strength of the ongoing price trend.
- **Average Directional Index (ADX)**: Filters out weak, low-momentum setups when trend strength falls below predefined thresholds.
- **Bollinger Band Width (BBW)**: Identifies volatility squeeze and expansion phases to time explosive directional breakouts.
- **Volume Climax Multiplier**: Detects localized institutional volume surges relative to rolling baseline averages.
- **Candlestick Solid Body Ratio**: Ensures price action momentum confirms directional sentiment before triggering order fills.

---

## Live Verifications & TradingView Strategy Reports

The strategy logic has been implemented and backtested on TradingView using Pine Script across various asset classes and timeframes:

- **Bitcoin (BTC/USDT) - 5-Minute Timeframe**: [View Pine Script & Performance Report](https://tw.tradingview.com/script/GXHAndCV/)
- **Semiconductor ETF (SOXX) - Daily Timeframe**: [View Pine Script & Performance Report](https://tw.tradingview.com/script/K1onF9Jv/)

---

## Interface & Execution Logs

### 1. Live Execution & Order Placement
Terminal execution logs showing real-time market data retrieval, state evaluation, and order fulfillment:
<img width="1131" height="657" alt="Terminal Execution Log 1" src="https://github.com/user-attachments/assets/f52a1d2f-d21b-4099-8364-11f55e5cf7a5" />
<img width="1658" height="221" alt="Terminal Execution Log 2" src="https://github.com/user-attachments/assets/040bbb4d-6102-4615-a61b-03f5a0912e60" />

### 2. Strategy Visualizations on TradingView
Signal triggers, entry levels, and profit-target executions visualised on interactive chart layouts:
<img width="1838" height="855" alt="TradingView Chart Setup 1" src="https://github.com/user-attachments/assets/d5231df1-1589-490f-bfa3-b7bab4d3fd28" />
<img width="1842" height="911" alt="TradingView Chart Setup 2" src="https://github.com/user-attachments/assets/3032c7ee-706e-424e-a889-65bebbc69ad6" />

### 3. Hyperparameter Optimization Results
Parameter sweep and objective convergence graphs evaluated via Optuna:
<img width="590" height="383" alt="Optuna Parameter Distribution" src="https://github.com/user-attachments/assets/6c01aec9-c6da-4b26-a629-1591188ec483" />
<img width="603" height="402" alt="Convergence Optimization Curve" src="https://github.com/user-attachments/assets/ce85aa9c-d995-4cf9-85d1-03d58913dcf6" />

---

## Risk Management & Order Execution

- **Single Position Constraint**: Strictly maintains at most one open long or short position at any given timestamp, preventing margin overexposure.
- **Dynamic Risk Sizing**: Configured with a default risk allocation (e.g., $1,500 trade quantity on a $300 capital base with predefined leverage controls).
- **Hard Stop-Loss (SL) & Take-Profit (TP)**: Automatic order cancellation and exit triggers enforced by percentage thresholds and absolute price movement bounds (`MAX_LOSS_PTS`, `MIN_MOVE_PTS`).
- **Friction & Fee Modeling**: Accounts for bilateral exchange commissions (default: 0.04% per side) to provide realistic net-of-fee performance metrics.

---

## Tech Stack

- **Core Runtime**: Python 3.9+
- **Performance & Optimization**:
  - `numba` (Just-In-Time compilation to native machine code)
  - `optuna` (Bayesian optimization of indicator thresholds)
- **Data & Quantitative Analysis**:
  - `pandas`, `numpy` (Vectorized tabular computations)
  - `pandas_ta` (Technical analysis library)
- **Exchange Integration**:
  - `ccxt` (Unified cryptocurrency exchange API)

---

## Installation & Usage

### 1. Installation
Clone the repository and install required packages:
```bash
git clone https://github.com/Kylechen0815/High-Performance-Quantitative-Trading.git
cd High-Performance-Quantitative-Trading
pip install ccxt pandas pandas_ta numpy colorama optuna numba
