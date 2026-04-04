# AI Trading Assistant — Feature Request

> **Dato:** 2026-04-04  
> **Fra:** FiWa  
> **Projekt:** aktieprojekt (stockmarket)

---

## Vision

En AI-drevet handels-assistent der giver **konkrete købsanbefalinger** med:
- Budget (hvor meget af kontantbeholdning at bruge)
- Gebyrer inkluderet (Nordnet: 0.15% min 99 DKK)
- Teknisk analyse (entry, stop-loss)
- Nyheder at holde øje med
- HO agent integration

---

## Eksempel: XOP Aktie

```
💰 KONTANT: 15.000 DKK

📊 ANALYSE: XOP (Olie/Energy)

💡 ANBEFALING:
"Køb for 9.953 DKK + 99 DKK (Nordnet gebyr) + USD konvertering = ~10.258 DKK"

📈 TEKNISK:
- Entry: ~170 DKK
- Stop-loss: ~162 DKK (-5% fra entry)
- Tidshorisont: 3-6 måneder
- ATR: 3.2% (volatilitet)

⚠️ STOP-LOSS LOGIK:
"Sæt stop-loss ved 162 DKK. Hvis aktien falder 5% 
fra entry, er risk/reward ikke optimal. 
Stop-loss beskytter mod tab > 500 DKK."

📰 NYHEDER AT HOLDE ØJE MED:
- OPEC møder (kvartalsvis)
- US rig count (ugevis)
- Crude oil inventory data (onsdag)

🔗 HO AGENT:
"Forbindelse til HO → Research agent henter 
seneste nyheder + tekniske indikatorer automatisk"
```

---

## Gebyr-beregner (Nordnet DK)

| Type | Gebyr |
|------|-------|
| Kurtage (DK aktier) | 0.15%, min 99 DKK |
| USD/DKK konvertering | ~0.3% |
| Depot | 0 DKK |

**Eksempel: Køb XOP for $73 (≈170 DKK)**
```
Aktie: 10 stk × 170 DKK = 1.700 DKK
Kurtage: 1.700 × 0.15% = 2.55 DKK (min 99) = 99 DKK
USD konvertering: ~5 DKK
─────────────────────────────────
TOTAL: ~1.804 DKK
```

---

## UI Flow

```
┌─────────────────────────────────────┐
│  PORTFOLIO OVERBLIK                │
│  💰 Kontant: [15.000 DKK]         │
│  📈 Total værdi: [XX.XXX DKK]     │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  AKTIE-LISTE                       │
│  AAPL  |  +2.3%  |  [ANALYSE]     │
│  XOP   |  -1.2%  |  [ANALYSE]     │  ← Tryk på XOP
│  GSPC  |  +0.8%  |  [ANALYSE]     │
└─────────────────────────────────────┘
              ↓ (XOP valgt)
┌─────────────────────────────────────┐
│  AI ANBEFALING: XOP                │
│                                     │
│  💰 Købsanbefaling:                │
│  "Køb for 10.258 DKK (inkl. gebyr)"│
│                                     │
│  📊 Teknisk:                      │
│  Entry: 170 DKK                    │
│  Stop-loss: 162 DKK (-5%)          │
│                                     │
│  📰 Nyheder: [Læs seneste]       │
│                                     │
│  [BEKRÆFT HANDEL]                  │
└─────────────────────────────────────┘
```

---

## HO Agent Integration

```
Bruger trykker XOP
        ↓
HO → Rex: "Research XOP technical + news"
HO → Max: "Analyze budget + recommendation"
HO → Gema: "Build trading UI component"
HO → Valo: "QA recommendation"
        ↓
Gem → Fjwa: "Her er din anbefaling..."
```

---

## Tekniske Kilder

- **Nordnet gebyrer:** research/nordnet_research_001.md
- **Dashboard design:** research/dashboard_flow_001.md

---

## Next Steps

1. [ ] Opret UI mockup i aktieprojekt
2. [ ] Byg "Kontant beholdning" input
3. [ ] Byg AI anbefalings-panel
4. [ ] Integrer Nordnet gebyr-beregner
5. [ ] Test med HO agent flow

---

*Request from FiWa | 2026-04-04*
