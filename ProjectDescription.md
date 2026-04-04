# 🎯 ProjectDescription: Aktieprojekt

## Målsætning

Automatiseret ETF-overvågning med teknisk analyse til at identificere købs- og salgssignaler.

## Delmål (fra FiWa, 2026-03-31)

1. **1. Delmål:** Et aktie/ETF overvågningsværktøj der med .py API + OpenClaw analyserer og anbefaler køb/salg bedre end Dansk C20 index. Løbende iteration og forbedring over 1 måned.
2. **2. Delmål:** Når 1. måned er bevist bedre end C20 (inkl. handelsomkostning jf. Nordnets regler) laver vi en test måned med 10.000kr. Nordnet har lukket for API adgang = daglig rutine med tjek og manuel køb via FIWA.
3. **3. Delmål:** Når de 2 måneder er gået med løbende iterativ forbedringer og bevist bedre afkast end C20, finder vi en handelsplatform hvor der kan købes og sælges via API og aktiebot.

## Status

**Phase:** 1 - Aktiv udvikling (Dag 4/30)

## Nordnet Research (2026-04-04)

### Nordnet API
- Officiel API v2 eksisterer (GitHub: nordnet/next-api-v2-examples)
- Kræver kontakt til Nordnet - ikke selvbetjent
- Python 3 eksempler tilgængelige
- Alternativ: Infront Active Trader (14 dage gratis prøve)

### Nordnet Gebyrer (DK)
- Kurtage: 0.15%, min 99 DKK (Nasdaq Copenhagen)
- Depotgebyr: 0 DKK
- Kurtagefri: Udvalgte danske aktier + investeringsforeninger

### Anbefalingsstruktur
- Rating (Køb/Salg/Hold)
- Kursmål + tidshorisont
- Risiko (Low/Medium/High)
- MiFID II compliance + disclaimers

---

## Ticker Universe
XOP, OIH, IYE, VDE, XLE, USO, BNO, ITA, PPA, XAR, GLD, IAU
(energi, olie-proxies, forsvar, guld)

## Indikatorer
- SMA50, SMA200, ATR(14), RSI(14), Donchian(20/55)

## Setups
- **Trend køb:** Pris > SMA50 > SMA200, positiv SMA200-hældning, RSI 50–70
- **Pullback køb:** Optrend + pris nær SMA50 (±1×ATR) + close > gårsdagens high + RSI 35–55
- **Kanal-/range-brud:** Close > forrige Donchian-55 High

## Risikomodel
- Initialt stop: close – max(2×ATR, 3% af pris)
- TP1/TP2: ≈2R og 3R
- Position sizing: 1% af konto-kapital (justerbar)
- Volatilitet: ATR% klassificering (lav/middel/høj)

## Data & Output
- Yahoo Finance via yfinance
- Farvekodet tabel (grøn=KØBEKLAR, gul=AFVENT)
- Log til etf_monitor_log.csv

## FIXME / Ønsker
- **Defaults:** Scriptet skal kunne køre med `python etf_monitor.py` uden arguments (aktuelt skal man angive --equity og --risk-pct)
- Miljøvariable support: ACCOUNT_EQUITY, RISK_PCT

---

*Created: 2026-03-31 by HB*
