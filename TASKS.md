# TASKS.md — Aktieprojekt

## OPGAVELISTE

### ETF Monitor: Default parametre
- **Status:** completed
- **Type:** 🟢
- **Created:** 2026-03-31
- **Description:** Tilføj default værdier så scriptet kan køre med `python etf_monitor.py` uden --equity/--risk-pct. Understøt ACCOUNT_EQUITY og RISK_PCT som miljøvariable.
- **Next step:** Læs etf_monitor.py, find hardcoded værdier, tilføj defaults + env var support
- **Result:** ✅ DEFAULT_EQUITY=200000, DEFAULT_RISK_PCT=0.75 + yfinance multi-level column bug fixed + datetime deprecation fixed. Testet OK: 7 købssignaler.

### ETF Monitor: Pin projektbeskrivelse i kanal
- **Status:** completed
- **Type:** 🔴 FIWA
- **Created:** 2026-03-31
- **Description:** Pin ProjectDescription i #aktieprojekt kanalen så andre kan se målsætningen
- **Next step:** FIWA - skal pilles i kanalen af dig (bot can't pin)
- **Result:** ✅ 2026-04-04 - HB status besked pinnet (bot KAN pinne!)

---

## 🔴 FIWA — Afventer beslutning

*(ingen for nu)*

### ETF Monitor: Koer rapport (loerdag reference)
- **Status:** completed
- **Type:** 🟢
- **Created:** 2026-04-04
- **Description:** Koer `python etf_monitor.py --once` og gem resultat som referencerapport. Selvom markedet er lukket (loerdag), kan vi se sidste lukkekurser og have en baseline.
- **Next step:** cd projects/aktieprojekt && python etf_monitor.py --once
- **Result:** 7x KOEBEKLR (XOP,OIH,IYE,VDE,XLE,USO,BNO) - Trend/Breakout | 5x AFVENT (ITA,PPA,XAR,GLD,IAU) | Encoding bug (colorama convert=False) fixed

### ETF Monitor: C20 benchmark sammenligning
- **Status:** completed
- **Type:** 🟡
- **Created:** 2026-04-04
- **Description:** Hent C20 (OMXC20) data via yfinance og sammenlign relativt. Vis hvordan ETFerne performer vs. C20 over samme periode. Dokumenter i benchmark.md.
- **Next step:** Resultat: USO +96%, BNO +88%, XOP +40% vs C20 -6.4% (3 mdr)
- **Result:** ✅ 2026-04-04 - Olie/energi outperformer C20 markant

### ETF Monitor: HTML dashboard (light mode)
- **Status:** completed
- **Type:** 🟡
- **Created:** 2026-04-04
- **Description:** Lav et enkelt HTML dashboard der viser ETF status med farvekodning. Kan aabnes i browser og gjoer det nemmere at dele med andre.
- **Next step:** Design simpel HTML tabel med samme farvekoder som CLI versionen
- **Result:** ✅ 2026-04-04 - dashboard.html oprettet med ETF tabel + benchmark oversigt

### Dashboard: Opdater med live data fra script
- **Status:** pending
- **Type:** 🟢
- **Created:** 2026-04-04
- **Description:** Dashboard.html bruger static sample data. Kør etf_monitor.py og opdater dashboard med faktiske værdier for alle ETF'ere (RSI, ATR%, volatilitet, stop/TP1).
- **Next step:** cd projects/aktieprojekt && python etf_monitor.py --once > output.json (eller parse stdout) → opdater dashboard.html
- **Result:** 

### Strategi: Backtest af Trend køb setup
- **Status:** completed
- **Type:** 🟡
- **Created:** 2026-04-04
- **Description:** Backtest Trend køb setup (SMA50>SMA200, RSI 50-70) over 3 år for at måle winrate, avg trade, max drawdown. Brug yfinance historical data.
- **Next step:** Design backtestfunktion der loader historiske kurser ogsimulerer trades baseret på setupregler
- **Result:** ✅ 2026-04-04 - backtest_trend.py kørt. 214 trades (12 tickers, 3 år). Winrate 30.4%, avg R 0.53, avg retur +30.7%. GLD/IAU +86%, VDE/IYE negative. 

### Feature: Signal-alert via Discord
- **Status:** pending
- **Type:** 🔵
- **Created:** 2026-04-04
- **Description:** Når scriptet kører i loop, og en ETF skifter fra AFVENT til KØBEKLAR (eller omvendt), send besked til #aktieprojekt kanalen automatisk.
- **Next step:** Undersøg mulighed for at sende Discord besked via bot når signal ændres
- **Result:** 

### Feature: Portefølje-tracker (CSV log over tid)
- **Status:** pending
- **Type:** 🟡
- **Created:** 2026-04-04
- **Description:** Udvid etf_monitor_log.csv til at inkludere alle trades (buy/sell/hold) med position sizing, R-multiple, og akkumuleret P&L over tid. Lav et simpelt chart der viser equity curve.
- **Next step:** Design CSV-schema med kolonner: date, ticker, signal, entry_price, exit_price, position_size, PnL, R_multiple, notes
- **Result:** 

---

*Created by HB 2026-03-31*
