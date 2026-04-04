# Portfolio Risk Management — Research 001
**Agent:** REX | **Dato:** 2026-04-04 | **Status:** Færdig

---

## 1. Positionsstørrelse baseret på risiko

- **Kerneprincippet:** Risiko, ikke kapital, bestemmer hvor meget man køber.
- **Volatilitetsbaseret sizing:** Brug aktivets daglige/ugentlige standardafvigelse (sigma) til at udregne positionsstørrelse.
  - Formel: `Position = RisikoBeløb / (EntryPrice - StopLossPrice)`
  - Eksempel: Konto på 100.000 kr, max tab 2% = 2.000 kr. Aktie købt til 100 kr, stop-loss på 95 kr → `2.000 / 5 = 400 aktier` = 40.000 kr eksponering.
- **ATR-baseret (Average True Range):** Mål aktivets typiske daglige udsving. Brug f.eks. 2× ATR som stop-loss afstand.
  - Mere dynamisk end fast procentsats — tilpasser sig aktivets naturlige volatilitet.
- **Risiko pr. trade:** Sæt en fast procentdel af porteføljen som max tab per handel (typisk 1-2%).
- **Max eksponering:** Begræns samlet eksponering i én aktie/sektor (f.eks. max 5-10% per position, max 20-30% i én sektor).
- **Kelly-delen (se afsnit 2):** Kelly-procentdelen giver et teoretisk optimum for positionsstørrelse givet forventet edge og win-rate.

---

## 2. Kelly Criterion

- **Hvad er det?** En matematisk formel til at beregne den optimale andel af kapital til at satse/håndtere i én position.
- **Den klassiske formel (binær version):**
  ```
  f* = (b × p - q) / b
  hvor:
    f* = Kelly-procentdel (fraction of bankroll)
    b  = netto-odds (gevinst/tab ratio, f.eks. 2:1 = 2)
    p  = sandsynlighed for gevinst (win rate)
    q  = sandsynlighed for tab = 1 - p
  ```
- **Forenklet version (når b=1, dvs. lige odds):** `f* = 2p - 1`
- **Eksempel:**
  - Win rate = 55% (p=0,55), odds = 1:1 (b=1)
  - Kelly% = (1×0,55 - 0,45)/1 = **10%** af kapitalen per handel
- **Kelly i praksis:** De fleste bruger **Half-Kelly** eller **Quarter-Kelly** (halvdele/kvart) for at reducere volatilitet og undgå overeksponering.
  - Half-Kelly i eksemplet ovenfor = 5% per handel.
- **Advarsler:**
  - Kelly forudsætter kendte, konstante odds — sjældent realistisk i aktiemarkedet.
  - Kræver p og b er estimeret korrekt; fejl i input giver massive fejlallokationer.
  - Brug kun som *vejledning*, ikke som facit.

---

## 3. Risk Parity vs Equal Weight

### Equal Weight (ligevægt)
- Hver position får samme andel af kapitalen (f.eks. 10 aktier = 10% hver).
- **Problemer:**
  - Ignorerer risiko — højvolatile aktier fylder lige så meget som stabile.
  - Kan give skæv portefølje hvis nogle aktier stiger markant (rebalancering nødvendig).

### Risk Parity (risikoparitet)
- Hver position bidrager **lige meget til den samlede porteføljerisiko**.
- **Sådan udregnes det:**
  1. Beregn risiko (varians/standardafvigelse) for hvert aktiv.
  2. Invers-vægt: `Vægt_i = (1/Risiko_i) / Σ(1/Risiko_j)` — lavere risiko = højere vægt.
  3. Eksempel: Aktie A (sigma=20%) og Aktie B (sigma=10%):
     - Invers: A=1/20=0,05, B=1/10=0,10 → Total=0,15
     - Vægt A = 0,05/0,15 = **33%**, Vægt B = 0,10/0,15 = **67%**
- **Fordele:**
  - Matcher risikobidraget på tværs af aktiver — bedre diversifikation.
  - Reducerer dominans fra højvolatile positioner.
- **Ulemper:**
  - Kræver løbende rebalancering (transaktionsomkostninger).
  - Stabilt aktiv kan ende med kæmpe vægt hvis andre aktiver bliver volatile.
  - Forudsætter at risikoestimater (varians) er rimeligt stabile over tid.

### Sammenligning
| Metode | Risikoorienteret | Kompleksitet | Typisk anvendelse |
|--------|-----------------|-------------|-------------------|
| Equal Weight | ❗ nej | Lav | Simpelt benchmark, passive investorer |
| Risk Parity | ✅ ja | Mellem | Professionelle, fondshåndtering |

---

## 4. Stop-Loss Strategier for Aktieporteføljer

- **Hvad er stop-loss?** En forudbestemt pris hvor du automatisk sælger for at begrænse tab.
- **Typer:**
  - **Fast stop-loss:** Sættes på forhånd (f.eks. 10% under købspris). Simpelt, men stift.
  - **Trailing stop:** Stoppen følger aktiekursen opad, låser gevinster ind men begrænser tab.
    - Eksempel: Købt til 100 kr, trailing stop på 10% → stop flytter til 110 hvis aktien stiger til 122,22 kr (stop altid 10% under peak).
  - **Tidsbaseret stop-loss:** Sælg hvis aktien ikke performer inden for X dage/uger (tidsstyring).
  - **Støttebaseret stop-loss:** Placer stoppet under teknisk støtte/zoneniveau.
  - **ATR-stop:** Stop baseret på aktivets ATR-værdi (følger volatilitet dynamisk).
- **Porteføljeniveau vs. enkeltaktie:**
  - *Enkeltaktie:* Typisk 5-15% max tab per position.
  - *Portefølje:* Hvis 5 aktier taber 10% hver = 50% samlet tab — overvej korrelationsstop (reducer hvis flere positioner taber samtidigt).
- **Taktisk brug:**
  - Sæsonbestemt stop: Luk spekulative positioner før sommer/ferieperioder (liquidity falder).
  - Nyhedsstop: Automatisk exit ved specifikke negative nyheder.
- **Advarsler:**
  - Stop-loss garanterer ikke en pris ved hurtige markedsbevægelser (gap down).
  - For tætte stops → hyppig "whipsaws" (udskiftning uden grund).
  - For løse stops → store tab.

---

## 5. Optimal Beholdning Baseret på Risikoprofil

- **Risikoprofiler (typisk inddeling):**

| Profil | Max Drawdown | Tidshorisont | Typisk strategi |
|--------|-------------|--------------|-----------------|
| Konservativ | 5-10% | Lang (>5 år) | lav volatile aktier, obligationer, stor dividende |
| Moderat | 15-25% | Mellem (3-5 år) | Balanceportefølje, blue chips, nogle growth |
| Aggressiv | 30-50% | Kort (<3 år) | Growth, små-cap, højbeta, gearede produkter |

- **Sharpe-ratio tilgang:** Mål risk-adjusted return.
  - `Sharpe = (Forventet afkast - Risk-free rate) / Standardafvigelse`
  - Brug historisk Sharpe til at sammenligne aktivkombinationer.
- **Mean-Variance Optimization (Markowitz):**
  - Find den portefølje med højeste forventede afkast for et givet risikoniveau.
  - Problemet: Kræver præcise estimater af forventet afkast — små fejl giver store fejlallokationer.
- **Maximum Drawdown-begrebet:**
  - Definer max tilladt drawdown (f.eks. 20%) → beregn positionsstørrelse så sandsynligheden for at ramme den er acceptabel.
- **Kelly-porteføljen:** Anvend Kelly-fraction på porteføljeniveau:
  - Brug samlede win-rate og gennemsnitlig risiko/gevinst for porteføljen.
- **Praktisk opskrift (enkel model):**
  1. Bestem risikotolerance (max tab i % af portefølje).
  2. Estimer hver akties volatilitet (sigma) — brug 1-3 års historisk data.
  3. Sæt stop-loss per aktie baseret på sigma (f.eks. 2× sigma som max tab).
  4. Beregn positionsstørrelse: `Beløb = Risikobudget / (StopPct)`.
  5. Summér — sørg for at samlet eksponering < 100% (spar kontanter tilbage).
  6. Rebalance: Månedligt eller når en position > ±X% fra targetvægt.

---

## Kilder / Yderligere Læsning
- Kelly, J.L. (1956) — "A New Interpretation of Information Rate" (original Kelly-artikel)
- Ray Dalio — Risk Parity / All Weather Portfolio konceptet
- Van Tharp — Position Sizing (supertrader-serien)
- Investopedia: Risk Management, Kelly Criterion, Stop-Loss
- Portfolio Visualizer (online værktøj til backtesting)

---

*REX, research agent • 2026-04-04*
