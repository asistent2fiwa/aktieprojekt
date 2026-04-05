# Nordnet API – Research (april 2024)

> **STATUS: 🔴 CRITISK FUND**  
> Nordnet API accepterer IKKE nye brugere (per april 2024/2025)

---

## 1. Nordnet API – Tilgængelighed

- **Gratis?** ✅ Ja, API'en er gratis at bruge – ingen licensomkostninger
- **Dokumentation:** `nordnet.se/externalapi/docs`
- **Github eksempler:** `github.com/nordnet/next-api-v2-examples` (Python 3 + Java)
- **Version:** nExt API v2 (REST + websockets/feeds)
- **⚠️ STOPPER:** Nordnet skriver direkte på deres side:  
  *"Nordnet API is currently not onboarding new customers."*  
  → Nye ansøgninger accepteres **ikke**. Eksisterende brugere kan fortsat bruge den.

### Hvordan adgang fungerer (teoretisk)
- Kræver Ed25519 nøglepar (offentlig/privat nøgle)
- Upload offentlig nøgle via Nordnet Web → Profil → Indstillinger → API-nøgle
- Nordnet genererer en API nøgle (UUID)
- Login via `public.nordnet.dk/api/2/login/start` (DK)
- Brug session key + Basic Auth på alle requests
- Alle responses er JSON
- Sprog: `Accept-Language: da` for dansk

---

## 2. Hente beholdning / pension

### Medlemmer / Konto-oversigt
```
GET /api/2/accounts                    → alle konti (incl. pension)
GET /api/2/accounts/{accid}/orders      → ordrer
GET /api/2/accounts/{accid}/allorders   → alle ordrer
GET /api/2/instruments/{instrument_id}   → instrument info
GET /api/2/main_search                 → søg instrumenter
```

### Portefølje-beholdning
- Findes via `/api/2/accounts` → `accid` for default konto
- Typisk included i account-oversigten
- Nordnet dækker: aktier, ETF'er, fonde, pension (aldersopsparing)

### Pris-data
- Via **Public Feed** (WebSocket): subscribe på `price` events
- Kan ikke hentes via REST alene – kræver feed-forbindelse

---

## 3. Automatiske handler via Nordnet

- **Teoretisk muligt:** API understøtter `POST /api/2/orders` (place order)
- Eksempel ordre-body:
  ```json
  {
    "volume": 1,
    "side": "BUY",
    "order_type": "LIMIT",
    "currency": "SEK",
    "price": 123.45,
    "market_id": 11,
    "identifier": "101"
  }
  ```
- **Markeder:** Alle Nordnet's børser (Sverige, Norge, Danmark, Finland)
- **Tredjepartsløsninger:** Sifferkoll.se tilbyder certificeret automated trading via Nordnet API (siden 2016)
- **Krav:** Man skal have API-adgang (se pkt 1 – pt. lukket)

---

## 4. Alternativer hvis Nordnet ikke har API

| Alternativ | Type | Pris |备注 |
|---|---|---|---|
| **Saxo Partner API** | Officiel API | Gratis/abo | Fokus på aktier, ikke pension |
| **Nasdaq CSD / VP** | Officiel | Abo | Danmarks VP – direkte depotadgang |
| **Nord Pool (power)** | — | — | Ikke relevant |
| **Forvaltningsrobotter** | Tredjepart | — | Ex. June, Nordea Invest |
| **Gocapit** | Aggregator | — | Samler pension fra flere banker |
| **Insurely** | Åben banking | — | Bruger PSD2 til at hente pension |
| **Selv-script (Excel/VBA)** | Manuelt | Gratis | Exportér via Nordnet Excel-add-in |
| **Nordnet Excel-add-in** | Officielt værktøj | Gratis | Direkte data til Excel (ikke API) |

### PSD2 / Åben Banking (interessant!)
- EU's betalingsdirektiv – banker SKAL give tredjeparter adgang
- Tjenester som **Nordigen**, **Tink**, **Klarna/Klarna Open Banking** kan bruges
- Kræver at Nordnet er under PSD2 i Danmark – usikkert om Nordnet er obligatorisk omfattet for pension
- Insurely bruger PSD2 til at samle pension på tværs af udbydere

---

## 5. Scrape-muligheder (legalt?)

### ❌ Rå scraping af Nordnet
- **Regler:** GDPR + Nordnet's vilkår forbyder typisk automatisk dataindsamling
- **Risiko:** Account suspended, juridiske skridt, GDPR-bøder
- **Konklusion:** Ikke anbefalelsesværdigt

### ✅ Legale alternativer til scraping
1. **Nordnet Excel-add-in** – Officielt, gratis, lovligt
2. **Manuel export** – Download CSV/PDF fra Nordnet Netbank
3. **PSD2-aggregatorer** – Insurely, Nordigen (lovligt via åben banking)
4. **Skattestyrelsen (TastSelv)** – Pensionsoversigt via borger.dk

---

## 📋 Anbefaling til aktieprojektet

1. **Tjek Nordnet API status** – Måske genåbner de (tjek nordnet.dk/externalapi)
2. **Excel-add-in** er næstbedst → kan hente beholdning, men ikke automatisere handler
3. **PSD2 via Nordigen/Tink** → læs saldo/beholdning, men ikke handel
4. **Saxo API** → hvis det handler om fri handel uden Nordnet
5. **Manuel CSV-export** → fungerer altid, men ikke automatisk

---

*Research af REX, 2026-04-04*
