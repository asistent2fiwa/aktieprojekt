# ASIS ↔ KO Protocol

**Version:** 1.0  
**Dato:** 2026-04-05  
**Status:** DRAFT - Ventende FiWa validation

---

## Core Concept

```
FIWA ←→ ASIS ←→ KO ←→ WORKERS (REX/GEMA/VALO/MAX)
```

| Agent | Rolle | Ansvar |
|-------|-------|--------|
| **ASIS** | Forbindelse/Interface | Ping-pong, brainstorm, vurdering, præsentation |
| **KO** | Koordinator/Task Manager | Routing, prioritering, pipeline, kø-styring |
| **MAX** | Strategisk Arkitekt | Opgave-dekomponering, prompt-engineering, syntese |
| **REX/GEMA/VALO** | Workers | Execute research/coding/QA |

---

## Regler for Aktivitet

### REGEL 1: Ping-Pong (ASIS ↔ FIWA)

**HVAD:** Privat samtale - ingen KO involvering.

**HVDAN:** Alt hvad der kan besvares i 5-10 sekunder.

**EXAMPLES:**
- "hvad synes du?" / "kan du forklare..."
- "hvem skrev..." / "hvad betyder..."
- Brainstorming, hurtige spørgsmål
- Daglig smalltalk

**REGLER:**
- ASIS svarer direkte
- Ingen logging til KO
- Ingen agenter spawnes

```
FIWA ←→ ASIS (KUN OS TO)
```

---

### REGEL 2: OPGAVE → KO Aktiveres

**HVAD:** Når FIWA gør noget til en egentlig opgave.

**SIGNALER:**
| Signal | Betydning |
|--------|-----------|
| "jeg **SKAL** lave..." | Opgave til KO |
| "**få lavet**..." | Opgave til KO |
| "**lav** den opgave..." | Opgave til KO |
| ASIS: "det her er for stort til 10 sek" | Eskalering |

**FLOW:**
```
FIWA: "jeg skal lave bachelor om svovlstikkerne"
       │
       ▼
  ASIS: "forslag til hvordan jeg definerer opgaven?"
       │
       ▼
  FIWA: "ja" / "nej, sådan her..."
       │
       ▼
  ASIS → KO: "NY OPGAVE: [beskrivelse], prioritet: HØJ/MELLEM/LAV"
       │
       ▼
  KO: Prioriterer + planner pipeline
       │
       ▼
  KO → MAX: "dekomponer denne opgave"
       │
       ▼
  MAX → KO: "her er 3-5 del-opgaver + prompts"
       │
       ▼
  KO → REX/GEMA/VALO: spawn workers
       │
       ▼
  [workers kører]
       │
       ▼
  KO → ASIS: "resultat klar / status opdatering"
       │
       ▼
  ASIS → FIWA: præsenterer
```

---

### REGEL 3: Status på Opgave

**HVAD:** FIWA spørger om status på en aktiv opgave.

**SIGNAL:** "status på [opgave]"

**FLOW:**
```
FIWA: "status på svovlstikkerne"
       │
       ▼
  ASIS → KO: "status?"
       │
       ▼
  KO: Samler status fra alle workers
       │
       ▼
  KO → ASIS: "
  1. REX:Hist FÆRDIG ✓ - Research på context done
  2. REX:Teori KØRER ████████░░ 80%
  3. REX:Biblio VENTER
  
  Forventet: 2-3 min"
       │
       ▼
  ASIS → FIWA: præsenterer status
```

---

### REGEL 4: HB/Cron → KO

**HVAD:** Heartbeat og Cron opgaver sendes til KO for prioritering.

**FLOW:**
```
HB: "opgave X fundet"
       │
       ▼
  HB → KO: "NY OPGAVE fra HB: [beskrivelse], prioritet: MELLEM"
       │
       ▼
  KO: Sætter i kø med andre opgaver
       │
       ├─ HØJ → starter med det samme
       ├─ MELLEM → i kø efter HØJ
       └─ LAV → når kapacitet ledig
```

**PRIORITETER:**
| Niveau | Betydning | Eksempel |
|--------|-----------|----------|
| HØJ | Akut, haster | Sikkerhedsproblemer, deadlines |
| MELLEM | Normal drift | Daglige checks, rapporter |
| LAV | Kan vente | Optimering, langsigtede projekter |

---

## Aktivitets-Tabel

| Input fra FIWA | ASIS gør | KO involveret? |
|----------------|----------|----------------|
| "hvad synes du?" | Svarer direkte | ❌ NEJ |
| "kan du forklare..." | Svarer direkte | ❌ NEJ |
| "hvem skrev..." | Svarer direkte | ❌ NEJ |
| Brainstorming | Diskuterer | ❌ NEJ |
| "jeg SKAL lave..." | Foreslår struktur | ✅ JA |
| "få lavet..." | Sender til KO | ✅ JA |
| ASIS: "for komplekst" | Eskalérer | ✅ JA |
| "status på..." | Spørger KO | ✅ JA |
| HB/Cron | Videresender | ✅ JA |

---

## KO Task States

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ QUEUED  │ ──→ │ ACTIVE  │ ──→ │ WAITING │ ──→ │ DONE    │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │               │               │
     └───────────────┴───────────────┘
                    │
                    ▼
              ┌─────────┐
              │ ERROR   │
              └─────────┘
```

| State | Betydning |
|-------|-----------|
| QUEUED | Ventende i kø |
| ACTIVE | Arbejdes på |
| WAITING | Venters på andre agenter |
| DONE | Færdig |
| ERROR | Fejl - eskaleres |

---

## Timeout & Retry

| Situation | Timeout | Retry |
|-----------|---------|-------|
| REX research | 2 min | 1 retry |
| GEMA coding | 5 min | 2 retries |
| VALO QA | 1 min | 1 retry |
| MAX synthesis | 3 min | 1 retry |
| KO total | 10 min | Eskalér til ASIS |

---

## Kommunikation KO ↔ ASIS

**Status beskeder:**
```
KO → ASIS: "OPGAVE_STARTET: [navn], ETA: [min]"
KO → ASIS: "OPGAVE_PROGRESS: [navn], 50% færdig"
KO → ASIS: "OPGAVE_DONE: [navn], fil: [path]"
KO → ASIS: "OPGAVE_ERROR: [navn], årsag: [info]"
```

---

*Sidst opdateret: 2026-04-05*
