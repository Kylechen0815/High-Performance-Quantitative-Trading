# High-Performance Quantitative Trading Backtesting & Multi-Indicator Optimization System

## Included making sell and buy, but holding one postion at a time.

This section of the repository focuses on live algorithmic trading execution. Built with Python and the `ccxt` (CryptoCurrency eXchange Trading Library) framework, this bot connects directly to cryptocurrency exchange APIs to fully automate the customized strategy described above.

###  Core Execution Features
- **Automated Order Placement:** Programmatically executes buy and sell orders based on real-time strategy signals without manual intervention.
- **Strict Position Management:** Enforces a rigid "hold one position at a time" rule. The bot will automatically verify current exposure and will not open concurrent positions, ensuring strict risk management.
- **Exchange Integration:** Leverages `ccxt` for secure, low-latency communication with exchange endpoints (e.g., Binance, Bybit) to fetch tickers, account balances, and create orders.

###  Live Execution & Order Logs

Below are the terminal execution logs demonstrating the bot successfully fetching market data, evaluating entry/exit conditions, and executing trades:

<img width="1131" height="657" alt="屏幕截图 2026-01-14 012730" src="https://github.com/user-attachments/assets/f52a1d2f-d21b-4099-8364-11f55e5cf7a5" />

<img width="1658" height="221" alt="屏幕截图 2026-01-14 012736" src="https://github.com/user-attachments/assets/040bbb4d-6102-4615-a61b-03f5a0912e60" />

###  TradingView interface

Bitcoin - 5min:

<img width="1838" height="855" alt="屏幕截图 2026-09-05 163302" src="https://github.com/user-attachments/assets/d5231df1-1589-490f-bfa3-b7bab4d3fd28" />

[click here to see report and scrpit](https://tw.tradingview.com/script/GXHAndCV/)

Stock - 1day:



## parameter optimized：

To ensure the strategy remains robust and adapts to different market regimes, a built-in parameter optimization module is included. It iterates through various combinations of indicator thresholds (e.g., ER length, R2, Climax Multiplier) to identify the most profitable and stable configurations before deploying live.

<img width="590" height="383" alt="屏幕截图 2026-01-23 010351" src="https://github.com/user-attachments/assets/6c01aec9-c6da-4b26-a629-1591188ec483" />

<img width="603" height="402" alt="image" src="https://github.com/user-attachments/assets/ce85aa9c-d995-4cf9-85d1-03d58913dcf6" />


