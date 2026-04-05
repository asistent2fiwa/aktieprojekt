# AI TRADING ASSISTANT — SPEC v3

> **Version:** 3.0  
> **Dato:** 2026-04-04  
> **FiWa Requirements Collected from Discord  

---

## 🎯 VISION

En **AI-drevet portefølje-assistent** der:
1. Giver **konkrete købsanbefalinger** med forklaring af beløb
2. Bruger **risk management** (Kelly, positionsstørrelse, stop-loss)
3. Holder øje med **alarmer** for holdings i risiko
4. Sender **7-dages nyhedsvarsler**
5. Integrerer med **Nordnet API** (fremtidig)

---

## 🔑 NØGLE-FEATURES

### 1. PORTFOLIO INPUT
```
💰 Kontant beholdning: [15.000 DKK] ← bruger kan redigere
📊 Total portefølje værdi: [AUTOMATISK]

Holdings tabel:
| Aktie | Stk | Købspris | Nu | +/-% | RSI | ATR |
|------|-----|----------|-----|------|-----|-----|
| XOP | 10 | 170 | 168 | -1.2% | 45 | 3.2 |
```

### 2. RISIKO-PARAMETRE (Redigerbare)
```
Max tab per trade: [2%] ← 2% af total
Stop-loss: [-5%] ← fast barrier
Kelly %: [10%] ← sikkerhedsmargin
Risk/Reward target: [1:3]
```

### 3. KØBSANBEFALING FORKLARING
**NØGLESPØRGSMÅL:** "Hvorfor præcis det beløb?"

**Svar bygget på risk management:**
```
💡 XOP ANALYSE

💰 KONTANT: 15.000 DKK

📊 ANBEFALING: "Køb for 10.258 DKK"

🔍 FORKLARING:
"10% max position (1.500 DKK) + 99 DKK Nordnet gebyr 
+ 0.3% USD konvertering = 10.258 DKK"

⚙️ RISIKO-BREAKDOWN:
• Max position (10%): 1.500 DKK ← Kelly 10% sikkerhed
• Stop-loss (-5%): Tab max 75 DKK 
• Risk/Reward (1:3): Potentiel gevinst 225 DKK
• Samlet risk: 0.5% af portefølje

🎯 STRATEGI:
• Entry: ~170 DKK
• Stop-loss: 162 DKK (-5%)  
• Take-profit: 185 DKK (+9%)
• Tidshorisont: 3-6 måneder

⚠️ ALARM-TRIGGERS:
• Stop-loss rammer ved 162 DKK → AUTOMATISK SLET
• Take-profit rammer ved 185 DKK → GEM GEVINST
• Volatilitet > 5% ATR → HOLD
```

### 4. ALARM-PANEL 🔔
```
🔔 AKTIVE ALARMER

1. ⚠️ XOP +8% (30 dage)
   "Nærmer sig 6-måneders peak - overvej at tage gevinst"
   → Kontekst: "Har holdt 4 måneder, target nået"

2. 🚨 AAPL -4% (idag)
   "Stop-loss niveau nærmer sig (162 DKK)"
   → Kontekst: "Nyheder: Fed rentemøde uge 15"

3. 📰 YDYDY - Nyhedsrisiko
   "Fed møde om 7 dage - mulig volatilitet"
   → Kontekst: "Anbefaling: Sælg 50% hvis > 5% fald"

4. 💎 NVDA - RSI < 30
   "Oversolgt - potentiel opgang"
   → Kontekst: "Købsområde iflg. Kelly formula"
```

### 5. TEKNISKE INDIKATORER
For hver aktie:
- **RSI (14)** — Oversolgt < 30, Overkøbt > 70
- **ATR (14)** — Volatilitet
- **SMA 20/50/200** — Trend
- **MACD** — Momentum
- **Support/Resistance** — Niveauer

### 6. 7-DAGES VARSEL
```
📅 DEN NÆSTE UGE

Mandag: OPEC møde (olieaktier: XOP, OIH)
Onsdag: US Jobless Claims (markedspåvirkning)
Torsdag: ECB rentemøde (EUR/USD)
Fredag: US Non-Farm Payrolls (arbejdsmarked)
```

---

## 🧮 FORMLER

### Positionsstørrelse
```
Position = (Portefølje × Risk%) / (Entry - Stop)
```

### Kelly Criterion
```
Kelly% = W - (1-W)/R
W = Win rate (f.eks. 0.55)
R = Risk/Reward ratio (f.eks. 3)
→ Brug 10% Kelly = 10% af optimal
```

### Gebyr-beregning (Nordnet)
```
Kurtage: max(0.15% × værdi, 99 DKK)
USD konvertering: ~0.3%
```

---

## 📁 FILER

| Fil | Indhold |
|-----|---------|
| `ai-trading-v3.html` | Main UI (TABS: Portfolio + AI + Alarms) |
| `research/risk_management_001.md` | Kelly, positionsstørrelse, stop-loss |
| `research/nordnet_research_001.md` | Nordnet gebyrer |
| `AI-TRADING-SPEC.md` | Denne spec |

---

## 🚀 ROADMAP

| Phase | Feature | Status |
|-------|---------|--------|
| v1 | Mockup | ✅ |
| v2 | Tabs + Alarmer | ✅ |
| v3 | Risk Management + Forklaring | 🔵 I PROGRESS |
| v4 | Nordnet API integration | 🔴 |
| v5 | Automatiske handler | 🔴 |

---

*Spec fra FiWa's Discord feedback | 2026-04-04*
