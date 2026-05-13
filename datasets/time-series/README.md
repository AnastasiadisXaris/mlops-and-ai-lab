# Time-Series Datasets

## Purpose

This folder stores datasets containing sequential or temporal information — sales history, web traffic, IoT telemetry, stock prices, energy consumption, and any data where the order of observations matters.

---

## Naming Convention

```text
<domain>-<description>-<frequency>-<version>.<ext>

# Examples:
sales-monthly-revenue-1m-v1.parquet
web-traffic-daily-sessions-1d-v1.parquet
iot-sensor-temperature-1h-v1.parquet
marketing-campaign-weekly-ctr-1w-v1.parquet
```

Frequency codes: `1m` (monthly) · `1w` (weekly) · `1d` (daily) · `1h` (hourly) · `1min` (minutely)

---

## Folder Structure

```text
time-series/
│
├── sales/                # sales and revenue data
├── web-analytics/        # traffic, sessions, conversions
├── marketing/            # campaign performance over time
├── iot/                  # sensor and telemetry data
├── finance/              # stock prices, economic indicators
└── synthetic/            # generated time-series for testing
```

---

## Schema

| Column | Type | Description | Example |
|---|---|---|---|
| timestamp | datetime | observation time | 2026-01-15 09:00:00 |
| value | float | measured quantity | 1250.75 |
| entity_id | string | series identifier (optional) | store_042 |
| frequency | string | data frequency | 1d |
| is_holiday | boolean | holiday flag (optional) | False |
| lag_1 | float | previous period value | 1198.30 |
| rolling_7d | float | 7-day rolling mean | 1215.40 |

---

## Key Concepts

### Stationarity

Most time-series models assume stationarity — constant mean and variance over time. Test and transform before modeling:

```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(df["value"].dropna())
print(f"ADF Statistic: {result[0]:.4f}")
print(f"p-value:       {result[1]:.4f}")
# p < 0.05 → stationary
```

### Lag Features

```python
import pandas as pd

df = df.sort_values("timestamp")
df["lag_1"]      = df["value"].shift(1)
df["lag_7"]      = df["value"].shift(7)
df["lag_30"]     = df["value"].shift(30)
df["rolling_7d"] = df["value"].rolling(7).mean()
df["rolling_30d"]= df["value"].rolling(30).mean()
df = df.dropna()
```

### Seasonality Decomposition

```python
from statsmodels.tsa.seasonal import seasonal_decompose

result = seasonal_decompose(df.set_index("timestamp")["value"],
                             model="additive", period=7)
result.plot()
```

---

## Train / Val / Test Split

**Always split chronologically — never randomly:**

```python
import pandas as pd

df = pd.read_parquet("datasets/time-series/sales/sales-daily-v1.parquet")
df = df.sort_values("timestamp").reset_index(drop=True)

n = len(df)
train = df.iloc[:int(n * 0.70)]
val   = df.iloc[int(n * 0.70):int(n * 0.85)]
test  = df.iloc[int(n * 0.85):]

print(f"Train: {train['timestamp'].min()} → {train['timestamp'].max()}")
print(f"Val:   {val['timestamp'].min()} → {val['timestamp'].max()}")
print(f"Test:  {test['timestamp'].min()} → {test['timestamp'].max()}")
```

---

## Recommended Models

| Model | Best For |
|---|---|
| ARIMA / SARIMA | univariate, stationary series |
| Prophet | trend + seasonality, missing data |
| LSTM | multivariate, complex patterns |
| Transformer | long-range dependencies |
| XGBoost + lags | tabular feature-based approach |
| N-BEATS | neural basis expansion |

---

## Evaluation Metrics

| Metric | Formula | Use Case |
|---|---|---|
| MAE | mean absolute error | interpretable error |
| RMSE | root mean squared error | penalizes large errors |
| MAPE | mean absolute percentage error | relative error |
| sMAPE | symmetric MAPE | avoids asymmetry |
| MASE | mean absolute scaled error | scale-independent |

---

## Common Public Datasets

| Dataset | Domain | Frequency |
|---|---|---|
| M4 Competition | mixed | hourly to yearly |
| ETT (ETTh1/ETTm1) | energy | hourly / 15-min |
| Air Passengers | aviation | monthly |
| NASDAQ / Yahoo Finance | finance | daily |
| Google Trends | web | weekly |

---

## Best Practices

- sort by timestamp before any operation
- split chronologically — never randomly
- create lag features after splitting to avoid leakage
- handle missing timestamps explicitly (forward fill or interpolation)
- document the data frequency and timezone in metadata

**Common pitfalls:** random splits leaking future data · creating lag features before splitting · ignoring missing timestamps · mixing frequencies without resampling · no stationarity check before ARIMA
