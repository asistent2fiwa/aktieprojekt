# Task Lifecycle

**Version:** 1.0  
**Dato:** 2026-04-05  
**Status:** DRAFT

---

## Complete Task Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                         FIWA                                     │
│  1. INPUT: "jeg skal lave bachelor om svovlstikkerne"           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         ASIS                                     │
│  2. VURDER: "dette er en kompleks opgave"                       │
│  3. FORSLÅ: "vil du have en disposition først?"                 │
│  4. FIWA BEKRÆFTER → ASIS → KO                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         KO (Koordinator)                         │
│  5. MODTAGER: "NY OPGAVE: bachelor svovlstikkerne"             │
│  6. TJEK: prioritet = HØJ (haster pga deadline?)              │
│  7. STATE: QUEUED → ACTIVE                                      │
│  8. SEND TIL MAX: "dekomponer denne opgave"                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         MAX (Arkitekt)                           │
│  9. ANALYSER: Opgavens omfang                                  │
│  10. DEKOMPONER: 4 del-opgaver                                 │
│  11. DESIGN: Prompts til hver agent                            │
│  12. KO: "klar til execution"                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         KO ( fortsat )                           │
│  13. SPAWN: REX:Hist (parallel)                                 │
│  14. SPAWN: REX:Teori (parallel)                               │
│  15. SPAWN: REX:Biblio (parallel)                              │
│  16. STATE: WAITING...                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ REX:Hist    │      │ REX:Teori  │      │ REX:Biblio  │
│ KØRER ████░░│      │ KØRER ██████│      │ VENTER ░░░░░│
└─────────────┘      └─────────────┘      └─────────────┘
         │                    │                    │
         ▼                    │                    │
    ┌─────────┐               │                    │
    │ DONE ✓  │               │                    │
    └─────────┘               │                    │
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         MAX (Syntese)                            │
│  17. MODTAGER: Resultater fra 3 REX agenter                    │
│  18. SYNTERISER: Til sammenhængende disposition                │
│  19. GEM: [fil]                                                │
│  20. KO: "OPGAVE DONE"                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         ASIS                                     │
│  21. MODTAGER: "resultat klar i [fil]"                         │
│  22. LÆSER: filen                                              │
│  23. PRÆSENTERER: til FIWA                                    │
│  24. SPØRGER: "vil du have en kortere version?"                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         FIWA                                     │
│  25. SVARER: "ja tak / nej tak"                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## State Transitions

```
                    ┌──────────────────────────────────────┐
                    │           OPGAVE OPRETTET           │
                    │         af FIWA eller HB/Cron        │
                    └──────────────────────────────────────┘
                                      │
                                      ▼
                    ┌──────────────────────────────────────┐
                    │              QUEUED                  │
                    │    Ventende i KO's prioritetskø    │
                    └──────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 │                 │
         ┌──────────────┐             │                 │
         │   ACTIVE     │             │                 │
         │  MAX kører   │             │                 │
         └──────────────┘             │                 │
                    │                 │                 │
                    ▼                 │                 │
         ┌──────────────┐             │                 │
         │  DECOMPOSED  │             │                 │
         │  Del-opgaver │             │                 │
         │  defineret   │             │                 │
         └──────────────┘             │                 │
                    │                 │                 │
         ┌──────────┼──────────┐      │                 │
         ▼          ▼          ▼      │                 │
    ┌─────────┐ ┌─────────┐ ┌─────────┐   │                 │
    │ WORKER1 │ │ WORKER2 │ │ WORKER3 │   │                 │
    │ KØRER   │ │ KØRER   │ │ KØRER   │   │                 │
    └─────────┘ └─────────┘ └─────────┘   │                 │
         │          │          │         │                 │
         └──────────┼──────────┘         │                 │
                    ▼                    │                 │
         ┌──────────────────────┐        │                 │
         │    WAITING           │        │                 │
         │  Alle workers venter │        │                 │
         │  på MAX syntese      │        │                 │
         └──────────────────────┘        │                 │
                    │                    │                 │
                    ▼                    │                 │
         ┌──────────────────────┐        │                 │
         │      SYNTESE         │        │                 │
         │   MAX samler alt     │        │                 │
         └──────────────────────┘        │                 │
                    │                    │                 │
                    ▼                    ▼                 ▼
         ┌──────────────────────────────────────────────┐
         │                   DONE                        │
         │  Resultat gemt, KO notificeret, ASIS klar    │
         └──────────────────────────────────────────────┘
```

---

## Opgave Object

```json
{
  "task_id": "uuid",
  "title": "Bachelor svovlstikkerne",
  "status": "DONE",
  "priority": "HØJ",
  "created_by": "FIWA",
  "created_at": "2026-04-05T21:00:00Z",
  
  "pipeline": {
    "steps": [
      {"agent": "REX:Hist", "status": "DONE", "output": "path/to/result1.md"},
      {"agent": "REX:Teori", "status": "DONE", "output": "path/to/result2.md"},
      {"agent": "REX:Biblio", "status": "DONE", "output": "path/to/result3.md"},
      {"agent": "MAX:Syntese", "status": "DONE", "output": "path/to/final.md"}
    ]
  },
  
  "progress": {
    "current": 4,
    "total": 4,
    "percent": 100
  },
  
  "eta_minutes": null,
  "actual_minutes": 3,
  
  "final_output": "path/to/final.md",
  "notified_to": "FIWA"
}
```

---

## KO Queue Management

### Prioritering

```python
PRIORITETER = {
    "HØJ": 1,      # Straks - overhaler alt
    "MELLEM": 2,   # Normal kø
    "LAV": 3       # Bagefter alt andet
}

# Eksempel kø:
# 1. [HØJ] Bachelor svovlstikkerne (FIWA)
# 2. [MELLEM] Daglig nyhedsoversigt (CRON)
# 3. [LAV] Optimér portfolio tracker (HB)
```

### Routing

```python
def route_to_agent(step):
    if step["agent"].startswith("REX"):
        return "researcher"
    elif step["agent"].startswith("GEMA"):
        return "coder"
    elif step["agent"].startswith("VALO"):
        return "qa"
    elif step["agent"].startswith("MAX"):
        return "synthesizer"
    else:
        return "unknown"
```

---

## Status Rapportering

### Til ASIS (indenfor 30 sek)

```
KO → ASIS: "
OPGAVE: Bachelor svovlstikkerne
STATUS: ████████░░ 75%

Del-opgaver:
1. REX:Hist ████████████ FÆRDIG ✓
2. REX:Teori ██████████░░ 80%
3. REX:Biblio ██████░░░░░ 40%

Forventet tid: ~1 min
"
```

### Til FIWA (via ASIS)

```
ASIS → FIWA: "
📚 Bachelor-disposition klar!

Jeg har lavet en disposition baseret på:
• Historisk kontekst (1845 Danmark)
• Teoretiske rammer (marxisme, fænomenologi)
• 6 centrale kilder

💾 Fil: 2026-04-05_svovlstikkerne_disposition.md

Vil du have mig at forkorte den til 1 side?
"
```

---

## Fejl-Håndtering

| Fejl | Handling | Resultat |
|------|----------|----------|
| REX timeout | Retry 1x | Hvis fail igen → fortsæt uden |
| MAX timeout | Retry 1x | Hvis fail → ASIS sampler selv |
| KO crash | Task overlever | Genstart KO, fortsæt |
| Worker dør | KO spawner ny | Fortsæt pipeline |

### Error States

```
┌─────────┐
│  ERROR  │ ← Midlertidig fejl, KO forsøger igen
└─────────┘
     │
     ├─ Retry lykkedes → WAITING → DONE
     │
     └─ Retry fejlede → 
            │
            ├─ Kritisk → ASIS → FIWA: "problemer med [opgave]"
            │
            └─ Ikke kritisk → Fortsæt uden den del
```

---

## Pipeline Eksempler

### Research Pipeline (REX only)
```
Opgave → REX:Hist + REX:Teori + REX:Biblio → MAX → DONE
```

### Coding Pipeline (GEMA + VALO)
```
Opgave → GEMA:Setup → GEMA:Core → GEMA:UI → VALO:QA → DONE
```

### Hybrid Pipeline (Alle)
```
Opgave → MAX:Plan → REX:Research → MAX:Syntese → GEMA:Build → VALO:QA → DONE
```

---

*Sidst opdateret: 2026-04-05*
