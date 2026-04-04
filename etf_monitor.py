# etf_monitor.py
# -*- coding: utf-8 -*-
"""
ETP/ETF Monitor for energy, defense and gold ETFs mentioned in the discussion.

Features
--------
- Pulls daily data using yfinance
- Calculates core indicators: SMA(50/200), ATR(14), RSI(14), Donchian channels (20/55)
- Derives three actionable setups in plain Danish:
  1) "Trend køb"  (trend-following when structure is bullish)
  2) "Pullback køb" (buy the dip within an uptrend near dynamic support)
  3) "Kanal-/range-brud" (Donchian 55 breakout)
- Prints human-friendly recommendations like:
  "Nu er denne X ETF købeklar pga 'YY element'. Anbefaling: sælg på 'ZZ' måde."
- Simple risk model: ATR-based stop, position sizing by % risk of equity
- Optional loop to keep watching during market hours

Usage
-----
1) Install dependencies (one-time):
   pip install --upgrade yfinance pandas numpy tabulate colorama pytz

2) Run once:
   python etf_monitor.py --once --equity 150000 --risk-pct 1.0

3) Run in loop (checks every 30 min by default while US market is open):
   python etf_monitor.py --equity 150000 --risk-pct 1.0 --sleep-minutes 30

Notes
-----
- Data source: Yahoo Finance via yfinance
- Markets: US-listed ETFs
- Timezone logic: US/Eastern market hours (09:30–16:00)

"""

from __future__ import annotations
import argparse
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import os

import numpy as np
import pandas as pd
from tabulate import tabulate
from colorama import Fore, Style, init as colorama_init
import pytz

# Fix Windows console encoding for UTF-8 symbols (like ≈)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import yfinance as yf
except Exception as e:
    print("yfinance is required. Install with: pip install yfinance")
    raise

# ----------------------------
# Configuration
# ----------------------------
TICKERS = [
    # Energy (E&P/services/sector)
    "XOP", "OIH", "IYE", "VDE", "XLE",
    # Oil price proxies (futures-based ETFs)
    "USO", "BNO",
    # Defense / Aerospace
    "ITA", "PPA", "XAR",
    # Gold
    "GLD", "IAU",
]

DEFAULT_EQUITY = float(os.getenv("ACCOUNT_EQUITY", 200_000))  # DKK or USD—this is unit-agnostic
DEFAULT_RISK_PCT = float(os.getenv("RISK_PCT", 0.75))  # percent per trade

US_EASTERN = pytz.timezone("US/Eastern")

# ----------------------------
# Indicator utilities
# ----------------------------

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Compute RSI (Wilder's)"""
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, -delta, 0.0)
    roll_up = pd.Series(gain, index=series.index).ewm(alpha=1/period, adjust=False).mean()
    roll_down = pd.Series(loss, index=series.index).ewm(alpha=1/period, adjust=False).mean()
    rs = roll_up / (roll_down + 1e-12)
    rsi_val = 100.0 - (100.0 / (1.0 + rs))
    return rsi_val


def atr(h: pd.Series, l: pd.Series, c: pd.Series, period: int = 14) -> pd.Series:
    """Average True Range (ATR) with Wilder smoothing."""
    prev_close = c.shift(1)
    tr1 = h - l
    tr2 = (h - prev_close).abs()
    tr3 = (l - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr_val = tr.ewm(alpha=1/period, adjust=False).mean()
    return atr_val


def slope(series: pd.Series, lookback: int = 20) -> float:
    """Simple slope approximation over 'lookback' periods."""
    if len(series.dropna()) < lookback + 1:
        return np.nan
    return float(series.iloc[-1] - series.iloc[-lookback]) / lookback


@dataclass
class Signal:
    ticker: str
    status: str  # 'KØBEKLAR – Trend' | 'KØBEKLAR – Pullback' | 'KØBEKLAR – Breakout' | 'AFVENT'
    reason: str
    close: float
    atr: float
    stop: float
    take_profit_1: float
    take_profit_2: float
    position_size: float
    risk_text: str


# ----------------------------
# Core logic
# ----------------------------

def fetch_history(ticker: str, period: str = "2y", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=False)
    if df.empty:
        raise RuntimeError(f"No data for {ticker}")
    # yfinance >= 1.0 returns multi-level columns (Price, Ticker); flatten them
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]
    # Use Adj Close where available, else Close
    if "Adj Close" in df.columns:
        df["AdjClose"] = df["Adj Close"]
    else:
        df["AdjClose"] = df["Close"]
    return df


def analyze_ticker(ticker: str, equity: float, risk_pct: float) -> Signal:
    df = fetch_history(ticker)

    # Indicators
    df["SMA50"] = df["AdjClose"].rolling(50).mean()
    df["SMA200"] = df["AdjClose"].rolling(200).mean()
    df["ATR14"] = atr(df["High"], df["Low"], df["AdjClose"], 14)
    df["RSI14"] = rsi(df["AdjClose"], 14)
    df["Donchian20_H"] = df["High"].rolling(20).max()
    df["Donchian20_L"] = df["Low"].rolling(20).min()
    df["Donchian55_H"] = df["High"].rolling(55).max()
    df["Donchian55_L"] = df["Low"].rolling(55).min()
    df["VOL20"] = df["Volume"].rolling(20).mean()
    df["VOL50"] = df["Volume"].rolling(50).mean()

    last = df.iloc[-1]
    prev = df.iloc[-2]

    close = float(last["AdjClose"])  # latest adjusted close
    atr_val = float(last["ATR14"]) if not np.isnan(last["ATR14"]) else float("nan")
    sma50 = float(last["SMA50"]) if not np.isnan(last["SMA50"]) else float("nan")
    sma200 = float(last["SMA200"]) if not np.isnan(last["SMA200"]) else float("nan")
    rsi14 = float(last["RSI14"]) if not np.isnan(last["RSI14"]) else float("nan")
    d55_prev_high = float(df["Donchian55_H"].iloc[-2]) if not np.isnan(df["Donchian55_H"].iloc[-2]) else float("nan")

    # Slope of SMA200 for trend health
    sma200_slope = slope(df["SMA200"].dropna(), lookback=20)

    # --- Signal Rules ---
    status = "AFVENT"
    reason = ""

    # 1) Trend køb
    cond_trend = (
        close > sma50 > sma200 and
        (sma200_slope is not np.nan and sma200_slope > 0) and
        50 <= rsi14 <= 70
    )
    if cond_trend:
        status = "KØBEKLAR – Trend"
        reason = "Pris > SMA50 > SMA200, SMA200 stiger og RSI mellem 50–70 (trendstyrke)"

    # 2) Pullback køb: pullback til SMA50 i optrend, trigger når close > gårsdagens high
    cond_uptrend = close > sma200 and sma50 > sma200 and (sma200_slope is not np.nan and sma200_slope > 0)
    near_sma50 = abs(close - sma50) <= (1.0 * atr_val) if not np.isnan(atr_val) and not np.isnan(sma50) else False
    trigger_pullback = close > float(prev["High"]) if not np.isnan(prev["High"]) else False
    cond_rsi_pb = 35 <= rsi14 <= 55

    if status == "AFVENT" and cond_uptrend and near_sma50 and trigger_pullback and cond_rsi_pb:
        status = "KØBEKLAR – Pullback"
        reason = "Optrend intakt, pullback tæt ved SMA50 med ATR‑støtte og 'close>gårsdagens high' som trigger"

    # 3) Kanal-/range-brud: Donchian 55 breakout
    cond_breakout = close > d55_prev_high if not np.isnan(d55_prev_high) else False
    if status == "AFVENT" and cond_breakout:
        status = "KØBEKLAR – Breakout"
        reason = "Luk over Donchian 55‑høj (range‑brud)"

    # Risk model (ATR-based). If ATR is NaN (not enough data), default to 5% of price for stop distance
    if np.isnan(atr_val) or atr_val <= 0:
        stop_distance = 0.05 * close
    else:
        stop_distance = max(2.0 * atr_val, 0.03 * close)  # at least 3% buffer

    initial_stop = round(close - stop_distance, 2)
    tp1 = round(close + 2.0 * (close - initial_stop), 2)  # ~2R
    tp2 = round(close + 3.0 * (close - initial_stop), 2)  # ~3R

    # Position sizing by risk
    risk_amount = (risk_pct / 100.0) * equity
    per_share_risk = max(close - initial_stop, 0.01)
    position_size = risk_amount / per_share_risk

    # Volatility classification
    atr_pct = (atr_val / close) * 100 if atr_val and close else np.nan
    if np.isnan(atr_pct):
        vol_text = "Volatilitet: ukendt (manglende ATR)."
    elif atr_pct >= 4.0:
        vol_text = f"Høj volatilitet (ATR {atr_pct:.2f}% af pris) — forvent større sving."
    elif atr_pct >= 2.0:
        vol_text = f"Middel volatilitet (ATR {atr_pct:.2f}%)."
    else:
        vol_text = f"Lav volatilitet (ATR {atr_pct:.2f}%)."

    # Exit policy guidance
    if status.startswith("KØBEKLAR"):
        risk_text = (
            "Anbefaling: sælg delvist ved TP1 (≈2R) og lad resten køre med 'Chandelier' trailing (≈3×ATR) "
            "eller under SMA50 ved 2 lukkedage. Hårdt stop ved initialt stop."
        )
    else:
        risk_text = (
            "Afvent: ingen købesignal. Overvåg SMA50/SMA200‑struktur og Donchian‑bånd for nyt setup. "
            + vol_text
        )

    return Signal(
        ticker=ticker,
        status=status,
        reason=reason,
        close=round(close, 2),
        atr=round(float(atr_val) if not np.isnan(atr_val) else 0.0, 2),
        stop=initial_stop,
        take_profit_1=tp1,
        take_profit_2=tp2,
        position_size=float(position_size),
        risk_text=risk_text,
    )


def market_open_now() -> bool:
    """Return True if US market is open now (simple approximation)."""
    now_et = datetime.now(US_EASTERN)
    if now_et.weekday() >= 5:  # Saturday/Sunday
        return False
    open_t = now_et.replace(hour=9, minute=30, second=0, microsecond=0)
    close_t = now_et.replace(hour=16, minute=0, second=0, microsecond=0)
    return open_t <= now_et <= close_t


def run_scan(equity: float, risk_pct: float) -> pd.DataFrame:
    signals = []
    for t in TICKERS:
        try:
            sig = analyze_ticker(t, equity=equity, risk_pct=risk_pct)
            signals.append(sig)
        except Exception as e:
            signals.append(Signal(
                ticker=t,
                status="FEJL",
                reason=f"Datafejl: {e}",
                close=float('nan'),
                atr=0.0,
                stop=float('nan'),
                take_profit_1=float('nan'),
                take_profit_2=float('nan'),
                position_size=0.0,
                risk_text=""
            ))
    # Convert to DataFrame
    rows = []
    for s in signals:
        rows.append({
            "Ticker": s.ticker,
            "Status": s.status,
            "Årsag": s.reason,
            "Luk": s.close,
            "ATR": s.atr,
            "Stop": s.stop,
            "TP1": s.take_profit_1,
            "TP2": s.take_profit_2,
            "Pos.størrelse (~stk)": int(s.position_size) if np.isfinite(s.position_size) else 0,
            "Kommentar": s.risk_text,
        })
    df = pd.DataFrame(rows)
    return df


def pretty_print(df: pd.DataFrame):
    colorama_init(convert=False, autoreset=True)
    colored_rows = []
    for _, r in df.iterrows():
        status = r["Status"]
        if isinstance(status, str) and status.startswith("KØBEKLAR"):
            status_col = Fore.GREEN + status + Style.RESET_ALL
        elif status == "AFVENT":
            status_col = Fore.YELLOW + status + Style.RESET_ALL
        elif status == "FEJL":
            status_col = Fore.RED + status + Style.RESET_ALL
        else:
            status_col = status
        rr = r.copy()
        rr["Status"] = status_col
        colored_rows.append(rr)
    print(tabulate(pd.DataFrame(colored_rows), headers="keys", tablefmt="github", showindex=False))


def write_log(df: pd.DataFrame):
    from datetime import timezone
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = df.copy()
    out.insert(0, "Timestamp_UTC", ts)
    log_path = "etf_monitor_log.csv"
    if not os.path.exists(log_path):
        out.to_csv(log_path, index=False)
    else:
        out.to_csv(log_path, mode='a', header=False, index=False)


def main():
    parser = argparse.ArgumentParser(description="ETF monitor for trend/pullback/breakout setups")
    parser.add_argument("--once", action="store_true", help="Run a single scan and exit")
    parser.add_argument("--sleep-minutes", type=int, default=30, help="Minutes between scans when looping")
    parser.add_argument("--equity", type=float, default=DEFAULT_EQUITY, help="Account equity (same units as price)")
    parser.add_argument("--risk-pct", type=float, default=DEFAULT_RISK_PCT, help="Risk per trade in percent of equity")
    args = parser.parse_args()

    if args.once:
        df = run_scan(equity=args.equity, risk_pct=args.risk_pct)
        pretty_print(df)
        write_log(df)
        return

    # Looping mode
    print("Starter overvågning... (Ctrl+C for stop)")
    while True:
        try:
            if market_open_now():
                df = run_scan(equity=args.equity, risk_pct=args.risk_pct)
                pretty_print(df)
                write_log(df)
            else:
                now_et = datetime.now(US_EASTERN).strftime("%Y-%m-%d %H:%M:%S %Z")
                print(f"Markedet er lukket ({now_et}). Venter...")
            time.sleep(max(60, args.sleep_minutes * 60))
        except KeyboardInterrupt:
            print("\nStopper overvågning.")
            break
        except Exception as e:
            print(f"Fejl i loop: {e}")
            time.sleep(120)


if __name__ == "__main__":
    main()
