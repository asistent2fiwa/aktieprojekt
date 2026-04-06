# WAL.md — Aktieprojekt

## PROJEKT LOG

### 2026-04-06 15:43 — FIWA: GÅ AMOK MODE
**Action:** FiWa gav grønt lys til at arbejde aggressivt på opgaver
**Reason:** FiWa sagde "jatak gå amok med opgaverne"
**Result:** Sætter 3+ sub-agenter i gang
**Next:** 
1. Fix filterStocks i v3 (IIFE problem)
2. Bulk download + period optimization i etf_monitor.py
3. Watchlist.csv feature

*Lokal tid: 15:43*
**Action:** Kørte etf_monitor.py --once, opdaterede dashboard.html med friske ATR/vol værdier fra 6/4. 7 KØBEKLAR, 5 AFVENT. Priser uændrede (søndag, marked lukket). ATR opdateret for alle 12 tickers.
**Reason:** 🟢 task "Dashboard: Opdater med live data" var top of pending list
**Result:** ✅ dashboard.html — ATR + vol klassificering opdateret
**Next:** Signal-alert via Discord eller Portefølje-tracker

*Lokal tid: 07:03*
**Action:** HB oprettede projektstruktur autonomt
**Channel:** #aktieprojekt (Discord)
**Folder:** projects/aktieprojekt/
**Reason:** Top channel under #open-projects (position 1)
**Result:** Projektstruktur oprettet

**Next:** Afventer godkendelse af projektbeskrivelse + laes eventuelle bilag (etf_monitor.py)

### 2026-03-31 19:10 — Default parametre opdateret
**Action:** Opdateret DEFAULT_EQUITY og DEFAULT_RISK_PCT i etf_monitor.py
**Reason:** FiWa oenskede scriptet koerbar med `python etf_monitor.py` uden arguments
**Result:**
- DEFAULT_EQUITY: 100_000 → 200_000
- DEFAULT_RISK_PCT: 1.0 → 0.75
- Miljoevariable support var allerede implementeret (ACCOUNT_EQUITY, RISK_PCT)
**Source:** logs/aktieprojekt/attachments/183456_etf_monitor.py (Discord bilag)
**Next:** Kopier script til projektmappe, test koersel

### HEARTBEAT: 19:15
PROJECT: aktieprojekt
ACTION: Projekt oprettet + defaults sat + yfinance bug fixed + testet
REASON: Top channel under #open-projects (position 1)
RESULT: Script virker! 7 KOEBEKLR, 5 AFVENT
NEXT: Afventer FIWA godkendelse af script

### 2026-04-04 05:32 — ProjectDescription opdateret med FiWa's 3 delmal
**Action:** Tilfojede FiWa's 3 delmal fra Discord (2026-03-31 19:47) til ProjectDescription.md
**Reason:** Delmalene var kun i Discord, ikke i projektbeskrivelsen
**Result:** ProjectDescription.md nu opdateret med komplet maalsaetning + fase
**Next:** Pin projektbeskrivelse i Discord (kraever FIWA) | Koer script mandag morgen

### 2026-04-04 06:34 — WAL encoding fix + IDLE THINKING
**Action:** Fixed WAL.md encoding corruption (danske tegn gaade i krydsfelter) + genererede nye ideer
**Reason:** WAL havde 6 consecutive edit failures pga encoding. Kun 🔴 FIWA opgaver tilbage.
**Result:**
- WAL filen genskrevet med ren UTF-8
- 3 nye ideer tilfoejet til TASKS.md
**Ideas Generated:**
1. 🟢 Koer etf_monitor.py og producer en ny rapport ( lords day - kan vaere fint reference)
2. 🟡 Lav C20/OMXC20 benchmark sammenligning - hent C20 data og vis relativ performance
3. 🟡 Forbedret HTML dashboard med lys/soegning

### 2026-04-04 06:34 — Encoding fix + rapport koert
**Action:** Fixed colorama Windows encoding bug + koert ETF rapport
**Reason:** WAL had 6 consecutive edit failures (encoding). Saturday morning - US market closed but Friday data available.
**Result:**
- Fixed colorama `convert=False` + stdout UTF-8 reconfigure in etf_monitor.py
- Rapport koert: 7 KOEBEKLR (XOP,OIH,IYE,VDE,XLE,USO,BNO) + 5 AFVENT (ITA,PPA,XAR,GLD,IAU)
- WAL encoding cleaned (danske tegn genoprettet)
**Next:** C20 benchmark sammenligning | FIWA: pin projektbeskrivelse

### 2026-04-04 10:02 — C20 benchmark analyse
**Action:** Kortte C20 benchmark analyse for 3-måneds perioden
**Reason:** Idle heartbeat - ingen 🟢🟡🔵 tilbage undtagen denne
**Result:**
- USO: +96.41% | BNO: +88.24% | XOP: +39.95%
- OIH: +28.03% | VDE: +28.41% | XLE: +27.19%
- C20 benchmark: -6.41%
- Olie/energi ETF'ere outperformer C20 markant
**Next:** HTML dashboard | FIWA: pin projektbeskrivelse

### 2026-04-04 11:04 — HTML Dashboard oprettet
**Action:** Oprettet dashboard.html med ETF status, farvekodet tabel + benchmark oversigt
**Reason:** Næste prioriteret opgave fra 10:02 heartbeat
**Result:** 
- Fil: projects/aktieprojekt/dashboard.html
- Viser 7 KØBEKLAR + 5 AFVENT med farvekoder
- Benchmark søjler: USO +96%, C20 -6.4%
- Static sample data (baseret på WAL benchmark tal)
**Next:** Kør evt. script og opdater dashboard med live data | FIWA: pin projektbeskrivelse

### 2026-04-04 14:32 — Dashboard opdateret med live data
**Action:** Kortte etf_monitor.py med live data og opdaterede dashboard.html med faktiske priser, ATR%, Stop/TP1/TP2 for alle 12 ETF'ere
**Reason:** Næste prioriteret opgave fra 11:04 heartbeat — dashboard brugte static sample data
**Result:**
- Dashboard nu med LIVE 2026-04-04 lukkekurser
- 7 KØBEKLAR: XOP($177.72), OIH($399.05), IYE($62.83), VDE($168.06), XLE($59.25), USO($137.92), BNO($54.12)
- 5 AFVENT: ITA, PPA, XAR, GLD, IAU
- ATR% og volatilitets-badges opdateret
- Stop/TP1 for alle positioner
**Next:** 🟡 Backtest strategi | 🔵 Discord signal alerts | 🟣 Portefølje-tracker

### 2026-04-04 19:05 — Backtest Trend køb setup COMPLETED
**Action:** Kørte backtest_trend.py over 3 år, 12 ETF'ere
**Reason:** HO 🟡 næste steg fra 14:32 heartbeat
**Result:**
- 214 total trades | Winrate: 30.4% | Avg R: 0.53
- Guld vinder: GLD +86%, IAU +86%
- Defense: PPA +53%, XAR +53%, ITA +45%
- Olie: OIH +31%, XOP +23%
- Tabere: VDE -11%, IYE -6.5%, USO -0.4%
- Max drawdown: 14.3% gennemsnit
- Scripts: backtest_trend.py + outputs/backtest_trades.csv + outputs/backtest_summary.json
**Next:** 🔵 Discord signal alerts | 🟡 Portefølje-tracker | FIWA: overvej guldETF univers

*Last updated: 2026-04-04 19:05*
