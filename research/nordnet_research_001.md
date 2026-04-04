# Nordnet Research 001 – API & Anbefalingspraksis

**Research agent:** REX  
**Dato:** 2026-04-04  
**Fokus:** Nordnet API muligheder + Præsentation af aktieanbefalinger

---

## 1. Nordnet API Status – Er det åbent for API adgang?

### Officiel API (Next API v2)
- ✅ Nordnet har en **External API v2** – deres officielle API til automateret handel
- 📂 Officielle kodeeksempler ligger på GitHub: `github.com/nordnet/next-api-v2-examples`
- 🐍 Python 3-eksempler er tilgængelige (og kun disse – ikke andre sprog i det officielle repo)
- 🔗 Link til API-info: `nordnet.se/se/tjanster/handelsapplikationer#nordnet-api`
- ℹ️ Nordnet tilbyder også **Infront Active Trader** – et professionelt værktøj med API-integration, 14 dages gratis prøveperiode

### Adgangskrav
- ❌ API'et er **ikke fuldt åbent/selvbetjent** – man skal være Nordnet-kunde og typisk have en aktiv konto
- 🏦 API'et er primært rettet mod **Active Trading-kunder** (dem der handler aktivt)
- 📧 Kontakt med Nordnet Support (010 583 3199) er nødvendig for API-adgang
- ⚠️ Ingen offentlig developer portal med API-nøgler tilgængeligt som f.eks. Binance eller Yahoo Finance

### Tredjeparts-integrationer
- AutoChartist, Hanza og lignende værktøjer bruger Nordnets API underliggende
- Der findes **uofficielle Python-biblioteker** bygget på Nordnets API af community'et
- ADVARSEL: Brug af uofficielle API'er kan stride mod Nordnets vilkår

### Kilder
- https://github.com/nordnet/next-api-v2-examples
- https://www.nordnet.se/se/tjanster/handelsapplikationer

---

## 2. Nordnet Handelsgebyrer og Regler (Danmark)

### Købs-/salgskurtage (Danmark)
- **Aktier på Nasdaq Copenhagen:** typisk 0,15% af handelsværdi, min. 99 DKK
- **Aktier på andre nordiske markeder:** varierer (Norge, Sverige, Finland)
- **USA-aktier:** typisk 0,10 USD per aktie eller procentvis afhængigt af volumen
- **ETF'er:** særskilte gebyrstrukturer

### Nordnet Monthly Saver (investeringsformer)
- 0 DKK i gebyr for Nordnet Monthly Saver (investeringsforeninger)
- Fondskøb via Nordnet har typisk 0 DKK i kurtage (men fondsselskabet kan have årlige omkostninger)

### Kurtagefri handel
- Udvalgte danske aktier kan handles **kurtagefrit** (0 DKK) – Nordnet opdaterer liste løbende
- Investeringsforeninger ( fonds ) handles ofte uden kurtage

### Depotgebyr
- **0 DKK** i depotgebyr hos Nordnet (konkurrencefordel)
- Valutaveksling: 0,25% i valutaspread ved køb af udenlandske værdipapirer

### Kilder
- https://www.nordnet.dk/priser-og-vilkar (stadig relevant – Nordnet har historisk haft 0 depotgebyr)

---

## 3. Købsanbefalinger – Bedste Praksis

### Indholdselementer
- ✅ **Kursmål** – tydeligt angivet med tidshorisont (kort/mellemlang/lang)
- ✅ **Tidshorisont** – altid eksplicit (f.eks. "12 måneders horisont")
- ✅ **Risiko/rating** – f.eks. 1-5 stjerner, low/medium/high risk
- ✅ **Bevisgrundlag** – nævn nøgletal (P/E, EPS-vækst, revenue growth)
- ✅ **Investeringsargument** – hvad er "story'en" i 2-3 sætninger
- ✅ **Komparatorer** – sammenlign med konkurrenter, sektor, indeks

### Struktur (som anbefalingstekst)
```
🏆 KØB: [Selskab] – [Kursmål] (nu: [nuværende pris])
📈 Investeringstese: [kort opsummering]
📊 Nøgletal: P/E [x], EPS-vækst [%], ROI [%]
⏰ Tidshorisont: [X] måneder
⚠️ Risiko: [Low/Medium/High]
```

### Gode formuleringer
- Brug aktiv form: "Vi anbefaler køb af..." ikke "Man kunne overveje..."
- Vær specifik: "Kursmål 450 kr." ikke "Kursen vil stige"
- Angiv din konfidens: "Høj overbevisning" / "Medium overbevisning"
- Forklar "hvorfor nu": hvad er katalysatoren?

### Kilder
- CFA Institute guidelines on investment recommendations
- Bloomberg Terminal best practices for equity research

---

## 4. Salgsanbefalinger – Bedste Praksis

### Indholdselementer
- ✅ **Anden afslutning** – "Sælg" er stærkere end "Reducer" – brug korrekt
- ✅ **Argument for salg** – hvad har ændret sig siden købsanbefalingen?
- ✅ **Alternativ** – hvad skal man hellere købe? (viser konstruktiv holdning)
- ✅ **Stop-loss niveau** – hvis ikke anbefalingen allerede var en stop-loss

### Typiske anbefalingsniveauer (standard finans):
| Rating | Betydning |
|--------|-----------|
| **Strong Buy / Køb** | Forventer markant outperformance |
| **Buy / Køb** | Forventer outperformance |
| **Hold / Hold** | Forventer markedsafkast |
| **Reduce / Reducer** | Forventer underperformance |
| **Sell / Sælg** | Forventer markant underperformance |

### Gode formuleringer
- Forklar hvad der **ændrede sig**: ny konkurrent, makroændring, strategisk fejl
- Undgå bare at sige "vi sælger" – forklar reason
- Sæt det i perspektiv: "Vi nedjusterer fra Køb til Hold grundet..."
- Vis altid alternativ: "Vi flytter kapital til [alternativ] i stedet"

### Kilder
- Refinitiv/StarMine rating standards
- CFA Institute ethical guidelines for analysts

---

## 5. AI-Driven Stock Recommendations – Best Practices

### Datakilder (typisk i produktions-AI)
- **Finansielle data:** Yahoo Finance API, Alpha Vantage, Polygon.io, Refinitiv
- **Nyheder/sentiment:** News API, Twitter/X data, Reddit (r/wallstreetbets), FinBERT
- **Teknisk analyse:** TA-Lib, Pandas TA, TradingView
- **Alternativ data:** Google Trends, Satelitdata, Credit card data

### AI-modeller i brug (2024)
- **Store sprogmodeller (LLM'er):** GPT-4, Claude til tekstanalyse og rapportskrivning
- **Kvantitative modeller:** Random Forest, LSTM, Gradient Boosting til prisprognoser
- **Sentiment-analyse:** FinBERT, VADER til finansielle tekster
- **Ensemble-metoder:** kombinerer fundamental + teknisk + sentiment

### Struktur for AI-genereret anbefaling
1. **Opsummering** (1 sætning): "Samlet vurdering: KØB med høj overbevisning"
2. **Fundamental analyse:** Nøgletal, sammenligning med konkurrenter
3. **Teknisk analyse:** Trend, støtte/modstand, RSI, glidende gennemsnit
4. **Sentiment:** Nyheder, social media, analytiker-konsensus
5. **Risiko:** Makro, selskabsspecifik, likviditetsrisiko
6. **Rating + kursmål:** Konfidensniveau

### Best practices for AI-anbefalingssystemer
- ✅ Brug **multiple modeller/data feeds** – aldrig kun én kilde
- ✅ Altid **menneskelig review** før publicering (AI → human-in-the-loop)
- ✅ Dokumentér **usikkerhed** eksplicit
- ✅ Undgå "black box" – brug forklarbare modeller hvor muligt
- ✅ Test mod **backtesting** før live brug
- ✅ Hold styr på **modeldrift** – markeder ændrer sig

### Kilder
- arXiv:2310.03714 (LLMs in Finance)
- Bloomberg GPT research (BloombergML)
- CFA Institute: AI in Investment Management (2024)

---

## 6. Risk Management i Præsentation af Anbefalinger

### Juridiske og Compliance-krav
- ⚠️ **Investeringsanbefalinger skal følge EU's MiFID II-regler**
- ⚠️ I Danmark: gælder for både professionelle og retail-kunder
- ⚠️ **Disclamer er obligatorisk** – "Dette er ikke investeringsrådgivning"
- ⚠️ Interessekonflikter skal oplyses (f.eks. ejerskab i omtalte selskaber)

### MiFID II-krav til anbefalinger
- Anbefalingstype: Køb/salg/hold + begrundelse
- Identitet af analytiker og udgiver
- Tidspunkt for offentliggørelse
- Kursmål og tidshorisont
- Risikoniveau

### Anbefalet risk disclaimer
```
⚠️ Anbefalingen er udelukkende baseret på AI-genereret analyse og 
er IKKE investeringsrådgivning. Al handel sker på egen risiko. 
Historisk afkast er ingen garanti for fremtidigt afkast.
```

### Risk management principper i præsentation
- ✅ Vis altid **worst case**-scenario
- ✅ Angiv **position size**-anbefaling (max X% af portefølje)
- ✅ Brug **stop-loss** som fast element i salgsanbefalinger
- ✅ Vær transparent om **modellens usikkerhed** (f.eks. "Model confidence: 68%")
- ✅ Undgå at love specifikke afkast – brug ranges ("forventning: +15-25%")
- ✅ Angiv altid **tidshorisont** – 3 måneders anbefaling ≠ 3 års anbefaling

### Diversifikation-anbefaling
- Aldrig mere end 5-10% i én aktie i en portefølje
- Aldrig mere end 20-30% i én sektor
- Balancér med defensive aktiver ved høj usikkerhed

### Kilder
- ESMA (European Securities and Markets Authority) – MiFID II guidelines
- Finanstilsynet.dk – danske regler for investeringsrådgivning
- SEC Rule 206(4)-1 (hvis aktier er amerikanske)

---

## 7. Samlet Vurdering – Hvad Bør Filip Vide?

### Nordnet API
- Officiel API **eksisterer** men kræver Nordnet-konto + aktiv handelsstatus
- Ikke et open developer API – skal kontaktes for adgang
- Python-biblioteker findes, men vær opmærksom på vilkår

### Præsentation af anbefalinger
- Fast format: Rating → Kursmål → Horisont → Risiko → Begrundelse
- Altid med disclaimer + MiFID II-compliance
- AI-anbefalinger skal have human review

### Næste skridt
- Kontakt Nordnet Support (010 583 3199) for at høre om API-adgang
- Overvej Nordnet Monthly Saver til automatiske opsparinger
- Brug Infront Active Trader hvis du vil bygge egne systemer oven på Nordnet

---

*Research afsluttet af REX | 2026-04-04*  
*Fil: nordnet_research_001.md | Projekt: aktieprojekt*
