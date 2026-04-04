# backtest_trend.py
# -*- coding: utf-8 -*-
"""
Backtest: Trend køb setup (SMA50>SMA200, SMA200 slope>0, RSI 50-70)
3-års historik | Yahoo Finance
Output: winrate, avg R-multiple, max drawdown, trades log
"""

from __future__ import annotations
import os, sys
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

TICKERS = ["XOP", "OIH", "IYE", "VDE", "XLE", "USO", "BNO", "ITA", "PPA", "XAR", "GLD", "IAU"]
END = datetime.now()
START = END - timedelta(days=3 * 365)
INTERVAL = "1d"
ATR_PERIOD = 14
RSI_PERIOD = 14
SMA50_P = 50
SMA200_P = 200
RSI_BUY_MIN, RSI_BUY_MAX = 50, 70
SMA_SLOPE_LB = 20  # lookback for SMA200 slope

def rsi_func(s: pd.Series, period: int = 14) -> pd.Series:
    delta = s.diff()
    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, -delta, 0.0)
    roll_up = pd.Series(gain, index=s.index).ewm(alpha=1/period, adjust=False).mean()
    roll_down = pd.Series(loss, index=s.index).ewm(alpha=1/period, adjust=False).mean()
    rs = roll_up / (roll_down + 1e-12)
    return 100.0 - (100.0 / (1.0 + rs))

def atr_func(h: pd.Series, l: pd.Series, c: pd.Series, period: int = 14) -> pd.Series:
    prev_close = c.shift(1)
    tr1 = h - l
    tr2 = (h - prev_close).abs()
    tr3 = (l - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.ewm(alpha=1/period, adjust=False).mean()

def slope(s: pd.Series, lookback: int = 20) -> pd.Series:
    """SMA slope: (current - value 'lookback' bars ago) / lookback"""
    return (s - s.shift(lookback)) / lookback

def backtest_ticker(ticker: str) -> dict:
    df = yf.download(ticker, start=START, end=END, interval=INTERVAL, progress=False, auto_adjust=False)
    if df.empty:
        return None
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]
    if "Adj Close" in df.columns:
        df["AdjClose"] = df["Adj Close"]
    else:
        df["AdjClose"] = df["Close"]

    df["SMA50"] = df["AdjClose"].rolling(SMA50_P).mean()
    df["SMA200"] = df["AdjClose"].rolling(SMA200_P).mean()
    df["RSI14"] = rsi_func(df["AdjClose"], RSI_PERIOD)
    df["ATR14"] = atr_func(df["High"], df["Low"], df["AdjClose"], ATR_PERIOD)
    df["SMA200_slope"] = slope(df["SMA200"], SMA_SLOPE_LB)

    # Drop rows before SMA200 is valid
    df = df.dropna(subset=["SMA200", "SMA50", "RSI14", "SMA200_slope"])

    trades = []
    in_position = False
    entry_price = entry_date = None
    stop_loss = None
    tp1 = tp2 = None
    peak_equity = 100_000
    max_drawdown = 0.0
    equity = 100_000.0
    trade_count = 0
    wins = 0
    losses = 0
    r_multiples = []

    for i in range(len(df)):
        row = df.iloc[i]
        close = float(row["AdjClose"])
        sma50 = float(row["SMA50"])
        sma200 = float(row["SMA200"])
        rsi14 = float(row["RSI14"])
        atr14 = float(row["ATR14"])
        sma200_slope = float(row["SMA200_slope"])
        date = df.index[i]

        if not in_position:
            # Entry: Trend køb
            if (close > sma50 > sma200 and sma200_slope > 0 and RSI_BUY_MIN <= rsi14 <= RSI_BUY_MAX):
                risk_distance = max(2.0 * atr14, 0.03 * close)
                entry_price = close
                stop_loss = round(close - risk_distance, 2)
                tp1 = round(close + 2.0 * risk_distance, 2)   # 2R
                tp2 = round(close + 3.0 * risk_distance, 2)   # 3R
                in_position = True
                entry_date = date
                trade_count += 1
        else:
            # Exit checks
            exit_reason = None
            exit_price = close

            if close <= stop_loss:
                exit_reason = "STOP"
                exit_price = stop_loss
            elif close >= tp2:
                exit_reason = "TP2"
            elif close >= tp1:
                # Exit 50% at TP1, keep 50% for TP2
                exit_reason = "TP1_PARTIAL"
            elif (close < sma50) or (sma50 <= sma200):
                # Trend broken
                exit_reason = "TREND_BREAK"

            if exit_reason:
                in_position = False
                if exit_reason == "STOP":
                    r_mult = (exit_price - entry_price) / (entry_price - stop_loss) * -1 if entry_price != stop_loss else 0
                    pnl_pct = (exit_price / entry_price - 1) * 100
                    losses += 1
                elif exit_reason == "TP1_PARTIAL":
                    r_mult = (tp1 - entry_price) / (entry_price - stop_loss)
                    pnl_pct = (exit_price / entry_price - 1) * 100
                    wins += 1
                else:  # TP2 or TREND_BREAK → close at current
                    risk_distance = entry_price - stop_loss
                    r_mult = (exit_price - entry_price) / risk_distance if risk_distance > 0 else 0
                    pnl_pct = (exit_price / entry_price - 1) * 100
                    if exit_reason == "TP2":
                        wins += 1
                    else:
                        # Trend break - could be win or loss
                        if r_mult >= 1:
                            wins += 1
                        else:
                            losses += 1

                r_multiples.append(r_mult)
                equity = equity * (1 + pnl_pct / 100)
                equity = max(equity, 0.01)
                drawdown = (peak_equity - equity) / peak_equity * 100
                max_drawdown = max(max_drawdown, drawdown)
                peak_equity = max(peak_equity, equity)

                trades.append({
                    "ticker": ticker,
                    "entry_date": entry_date.date() if hasattr(entry_date, 'date') else entry_date,
                    "entry_price": round(entry_price, 2),
                    "exit_date": date.date() if hasattr(date, 'date') else date,
                    "exit_price": round(exit_price, 2),
                    "exit_reason": exit_reason,
                    "R_multiple": round(r_mult, 2),
                    "PnL_pct": round(pnl_pct, 2),
                    "equity_after": round(equity, 2),
                })

                # Re-evaluate entry on same bar after exit (don't skip bars)
                # Re-check entry conditions for next bar (don't re-enter same bar)
                if i + 1 < len(df):
                    next_row = df.iloc[i + 1]
                    n_close = float(next_row["AdjClose"])
                    n_sma50 = float(next_row["SMA50"])
                    n_sma200 = float(next_row["SMA200"])
                    n_rsi = float(next_row["RSI14"])
                    n_slope = float(next_row["SMA200_slope"])
                    if (n_close > n_sma50 > n_sma200 and n_slope > 0 and RSI_BUY_MIN <= n_rsi <= RSI_BUY_MAX):
                        risk_distance = max(2.0 * float(next_row["ATR14"]), 0.03 * n_close)
                        entry_price = n_close
                        stop_loss = round(n_close - risk_distance, 2)
                        tp1 = round(n_close + 2.0 * risk_distance, 2)
                        tp2 = round(n_close + 3.0 * risk_distance, 2)
                        in_position = True
                        entry_date = df.index[i + 1]
                        trade_count += 1

    total = wins + losses
    winrate = wins / total * 100 if total > 0 else 0.0
    avg_r = np.mean(r_multiples) if r_multiples else 0
    avg_pnl = np.mean([t["PnL_pct"] for t in trades]) if trades else 0

    return {
        "ticker": ticker,
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "winrate_pct": round(winrate, 1),
        "avg_R": round(avg_r, 2),
        "avg_PnL_pct": round(avg_pnl, 2),
        "max_drawdown_pct": round(max_drawdown, 2),
        "final_equity": round(equity, 2),
        "total_return_pct": round((equity / 100_000 - 1) * 100, 2),
        "trades": trades,
    }

def main():
    results = []
    trades_all = []

    print(f"Backtest: Trend køb setup | {START.date()} til {END.date()} | {len(TICKERS)} tickers\n")

    for ticker in TICKERS:
        try:
            print(f"  {ticker}...", end=" ", flush=True)
            res = backtest_ticker(ticker)
            if res:
                results.append(res)
                trades_all.extend(res["trades"])
                s = res
                print(f"{s['total_trades']} trades | WR {s['winrate_pct']}% | avgR {s['avg_R']} | ret {s['total_return_pct']}%")
            else:
                print("ingen data")
        except Exception as e:
            print(f"FEJL: {e}")

    if not results:
        print("Ingen resultater.")
        return

    # Aggregate summary
    total_trades_all = sum(r["total_trades"] for r in results)
    total_wins = sum(r["wins"] for r in results)
    all_rmultiples = []
    for t in trades_all:
        all_rmultiples.append(t["R_multiple"])

    print("\n" + "="*60)
    print("SAMLET BACKTEST RESULTAT")
    print("="*60)
    print(f"Tickere testet : {len(results)}")
    print(f"Setup          : Trend køb (SMA50>SMA200, slope>0, RSI 50-70)")
    print(f"Periode        : {START.date()} – {END.date()}")
    print(f"Start kapital  : 100.000 | Risiko: 1% per trade")
    print("-"*60)
    print(f"Total trades   : {total_trades_all}")
    wr_str = f"{total_wins/total_trades_all*100:.1f}%" if total_trades_all > 0 else 'N/A'
    print(f"Winrate        : {wr_str}")
    print(f"Avg R-multiple : {np.mean(all_rmultiples):.2f}" if all_rmultiples else "Avg R: N/A")
    avg_return_all = np.mean([r["total_return_pct"] for r in results])
    avg_wr = np.mean([r["winrate_pct"] for r in results])
    avg_drawdown = np.mean([r["max_drawdown_pct"] for r in results])
    avg_equity_final = np.mean([r["final_equity"] for r in results])
    print(f"Avg retur %    : {avg_return_all:.1f}%")
    print(f"Avg drawdown   : {avg_drawdown:.1f}%")
    print(f"Final equity   : {avg_equity_final:.0f} (avg)")
    print("="*60)

    # Per-ticker table
    print("\nPER TICKER:")
    print(f"{'Ticker':<6} {'Trades':>6} {'WR%':>5} {'AvgR':>5} {'Ret%':>6} {'MaxDD%':>6} {'FinalEq':>9}")
    print("-"*44)
    for r in sorted(results, key=lambda x: x["total_return_pct"], reverse=True):
        print(f"{r['ticker']:<6} {r['total_trades']:>6} {r['winrate_pct']:>5} {r['avg_R']:>5} {r['total_return_pct']:>6} {r['max_drawdown_pct']:>6} {r['final_equity']:>9}")

    # Save trades to CSV
    if trades_all:
        df_trades = pd.DataFrame(trades_all)
        csv_path = "outputs/backtest_trades.csv"
        os.makedirs("outputs", exist_ok=True)
        df_trades.to_csv(csv_path, index=False)
        print(f"\nTrades gemt: {csv_path}")

    # Save summary
    summary = {r["ticker"]: {k: v for k, v in r.items() if k != "trades"} for r in results}
    import json
    summary_path = "outputs/backtest_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    print(f"Summary gemt: {summary_path}")

if __name__ == "__main__":
    main()
