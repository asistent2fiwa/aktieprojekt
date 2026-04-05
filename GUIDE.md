# GEMA AI Trading Assistant - Bruger Guide

## Hurtig Start (2 min)

### 1. Åbn siden
**URL:** https://asistent2fiwa.github.io/aktieprojekt/ai-trading-v3.html

### 2. Tilføj en aktie
1. Klik på **Portfolio** fanen
2. Klik på søgefeltet "Søg aktie..."
3. Skriv f.eks. "NOVO" eller "NVDA"
4. Klik på resultatet
5. Klik **Tilføj**

### 3. Se anbefaling
- Pris, RSI, Kelly %, Stop Loss, Take Profit vises automatisk
- GRØN = Køb, GUL = Hold, RØD = Sælg

---

## Faner

| Fane | Beskrivelse |
|------|-------------|
| 📊 ETF | ETF monitor med køb/sælg signaler |
| 💼 Portfolio | Dine gemte aktier |
| 🤖 AI Assistant | Søg og chat med aktie-anbefalinger |
| 🔔 Alarmer | Pris-alarmer du har sat |
| 💬 Chat | Samtale med GEMA |

---

## Sådan bruges Portfolio

### Tilføj aktie
1. Gå til Portfolio
2. Skriv i søgefeltet (f.eks. "Tesla" eller "TSLA")
3. Vælg fra dropdown
4. Klik **Tilføj til portefølje**

### Tilføj egen aktie
Hvis din aktie ikke findes:
1. Klik **+ Tilføj egen** under søgefeltet
2. Indtast symbol og navn
3. Klik **Tilføj**

### Se detaljer
Klik på en aktie i listen for at se:
- **RSI** - Relativ Styrke Index (under 30 = oversolgt, over 70 = overkøbt)
- **Kelly %** - Anbefalet størrelse af position
- **Stop Loss** - Salg hvis prisen falder til dette
- **Take Profit** - Målpris for salg

---

## AI Assistant

### Søg aktie
1. Gå til AI Assistant
2. Skriv i søgefeltet (f.eks. "Apple")
3. Klik på resultatet
4. Se AI-analyse med det samme!

### Chat kommandoer
Skriv i chatten:
- `kun danske` - Vis kun danske aktier
- `ETF foretrukket` - Fokus på ETF'er
- `lav risiko` / `medium risiko` / `høj risiko` - Sæt risikoniveau

---

## ETF Monitor

Her kan du se tekniske signaler for populære ETF'er:

| Signal | Betydning |
|--------|-----------|
| **KOEB** | God tid til at købe (RSI under 30) |
| **AFVENT** | Vent og se (RSI 30-70) |
| **SELL** | Overkøbt - tag profit (RSI over 70) |

Kolonner:
- **Pris** - Nuværende pris
- **RSI** - Relativ Styrke Index
- **Stop** - Stop loss niveau
- **Target** - Målpris

---

## Alarmer

### Opret alarm
1. Gå til Alarmer fanen
2. Klik **+ Opret alarm**
3. Vælg aktie
4. Sæt pris-grænse
5. Gem

### Alarm typer
- **Over** - Advarsel når prisen stiger over grænsen
- **Under** - Advarsel når prisen falder under grænsen

---

## Valuta

Valutakurser vises i headeren:
- USD/DKK
- EUR/DKK
- GBP/DKK

Disse opdateres automatisk.

---

## Fejlfinding

### Priser hentes ikke
- Tjek internet forbindelse
- Yahoo Finance kan være nede - prøv igen senere
- Cachede priser fra sidste fetch vises

### Søgning virker ikke
- Vent på at siden er fuldt loaded
- Prøv at trykke på dropdown pilen

### Alarmer virker ikke
- Alarmer tjekkes ved hver side opdatering
- For vigtige alarmer, tjek manuelt

---

## Tips

1. **Opdater priser** - Klik på 🔄 knappen i headeren
2. **Portfolio backup** - Data gemmes i din browser (localStorage)
3. **Eksporter** - Snart: PDF export af portefølje
4. **Mørk tema** - Siden er designet til mørk visning

---

## Kort overblik

```
┌─────────────────────────────────────────────────┐
│  GEMA 🤖        USD: 6.90  EUR: 7.45  GBP: 8.80│
├─────────────────────────────────────────────────┤
│  [📊 ETF] [💼 Portfolio] [🤖 AI] [🔔] [💬]   │
├─────────────────────────────────────────────────┤
│                                                 │
│  Din aktie Analyse                              │
│  ━━━━━━━━━━━━━━━━━━━━                           │
│  RSI: 45  Kelly: 2.3%                          │
│  Stop: 892  Target: 1.045                       │
│                                                 │
│  [GRØN ANBEFALING 🟢]                          │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Kontakt / Feedback

Har du spørgsmål eller forslag?
- Discord: FiWa
- Email: Asis.tent.2.fiwa@gmail.com

---

*Sidst opdateret: 2026-04-05*
