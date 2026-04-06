# Heartbeat ↔ KO Bridge Architecture

**Version:** 0.1  
**Dato:** 2026-04-06  
**Status:** SPEC - Klar til præsentation  
**Audience:** Ekstern AI review

---

## Executive Summary

Dette dokument beskriver et hybrid multi-agent system der kombinerer:

1. **Heartbeat (HB)** - Autonom projekt-orchestration per kanal/projekt
2. **Knowledge Orchestrator (KO)** - Central task queue med prioritering på tværs af kanaler
3. **ASIS** - Interface agent der koordinerer menneske ↔ system

**Målet:** Behold det bedste fra begge systemer - HB's autonomi og KO's prioritering.

---

## System Oversigt

```
┌─────────────────────────────────────────────────────────────────┐
│                         FIWA (Bruger)                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ASIS (Interface Agent)                      │
│  • Ping-pong dialog                                           │
│  • Vurderer kompleksitet                                      │
│  • Tilføjer til KO med prioritet                              │
│  • Præsenterer resultater                                     │
└─────────────────────────────────────────────────────────────────┘
                    │                       ▲
                    ▼                       │
┌───────────────────────────────┐  ┌─────────────────────────────┐
│   HEARTBEAT (HB)             │  │   KO QUEUE                  │
│   • Per-projekt autonomi     │  │   • Central task list       │
│   • WAL logging              │  │   • Prioriteret (HOJ/MDV/LAV)│
│   • Projekt-organisation      │  │   • Cross-channel           │
│   • Tilføjer til KO          │  │                             │
└───────────────────────────────┘  └─────────────────────────────┘
                    │                       ▲
                    │                       │
                    ▼                       │
         ┌──────────────────┐               │
         │  PROJEKT FOLDERS │               │
         │  • tasks.md       │               │
         │  • WAL.md         │               │
         │  • ProjectDesc.md │               │
         │  • [filer]       │               │
         └──────────────────┘               │
                                            │
                         ┌─────────────────┴─────────────┐
                         │  KO WORKER                   │
                         │  • Læser KO queue            │
                         │  • Spawner agenter            │
                         │  • Ruter resultater           │
                         └─────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              ┌─────────┐   ┌─────────┐   ┌─────────┐
              │   REX   │   │  GEMA   │   │  VALO   │
              │(Research)│   │(Coding) │   │   (QA)  │
              └─────────┘   └─────────┘   └─────────┘
```

---

## Kerne-Komponenter

### 1. HEARTBEAT (HB)

**Ansvarsområde:**
- Per-projekt autonomi
- WAL logging
- Projekt-organisering
- Tilføjer opgaver til KO

**Hvad HB GØR:**
1. Læser HEARTBEAT.md for instruktioner
2. Tjekker øverste projekt ( Discord channel position)
3. Udfører simple checks (WAL, tasks, logs)
4. Komplekse opgaver → Tilføjer til KO queue
5. Log til WAL.md
6. Discord status ved behov

**Hvad HB IKKE GØR:**
- Spawner ikke agenter direkte (bruger KO)
- Udfører ikke kode (kun loger/organiserer)

**Fordele Bevaret:**
- ✅ Autonom kontinuitet
- ✅ Per-projekt struktur (tasks.md, WAL.md, ProjectDesc.md)
- ✅ Pinned info i Discord kanaler
- ✅ 30 min intervals (kan øges)

---

### 2. KO QUEUE

**Ansvarsområde:**
- Central task list
- Prioritering
- Cross-channel routing

**Struktur:**
```json
{
  "version": 1,
  "tasks": [
    {
      "id": "task_20260406_1430_01",
      "type": "RESEARCH",
      "prompt": "Undersøg Nordnet API muligheder",
      "priority": "HOJ",
      "source": "ASIS",
      "source_channel": "1487251822019350658",
      "source_project": "aktieprojekt",
      "status": "PENDING",
      "created": "2026-04-06T14:30:00Z",
      "assigned_to": null,
      "assigned_at": null,
      "result": null,
      "completed_at": null
    }
  ],
  "workers": {
    "active": [],
    "available": ["REX", "GEMA", "VALO"]
  },
  "last_updated": "2026-04-06T14:30:00Z"
}
```

**Task Felter:**

| Felt | Beskrivelse |
|------|-------------|
| `id` | Unik task ID (timestamp + sekventiel) |
| `type` | RESEARCH / CODING / QA / SYNTHESIS |
| `prompt` | Opgave beskrivelse |
| `priority` | HOJ / MELLEM / LAV |
| `source` | Hvem tilføjede (ASIS / HB / FIWA) |
| `source_channel` | Discord channel ID |
| `source_project` | Projekt navn |
| `status` | PENDING / ASSIGNED / COMPLETED / FAILED |
| `assigned_to` | Worker type (REX/GEMA/VALO) |
| `result` | Resultat/text (ved completion) |

---

### 3. ASIS (Interface Agent)

**Ansvarsområde:**
- Bruger-dialog
- Kompleksitets-vurdering
- Prioriterings-beslutning

**Flow:**
```
FIWA: "undersøg Nordnet API"
         │
         ▼
    ASIS vurderer:
    - Simpel fakta? → Svarer direkte
    - Kompleks? → Tilføjer til KO med prioritet
         │
         ▼
    KO queue: {priority: MELLEM, source_channel: xxx}
```

**ASIS Kan:**
- Tilføje opgaver til KO
- Sætte prioritet
- Præsentere resultater
- Svare på simple spørgsmål direkte

---

### 4. KO WORKER

**Ansvarsområde:**
- Læser KO queue
- Spawner agenter
- Ruter resultater

**Funktion:**
```python
# Pseudocode
def worker_loop():
    while True:
        task = get_next_pending_task()  # Sorteret efter prioritet
        
        if task:
            worker_type = match_task_to_worker(task.type)
            result = spawn_agent(worker_type, task.prompt)
            
            # Gem resultat
            complete_task(task.id, result)
            
            # Notify ASIS i source channel
            notify_channel(task.source_channel, result)
        else:
            sleep(30)  # Check hvert 30 sek
```

---

## HB ↔ KO Integration Points

### Integration Point 1: HB → KO (Tilføj Opgaver)

**HB Tilføjer:**
```json
{
  "source": "HB",
  "source_channel": "1487251822019350658",
  "source_project": "aktieprojekt",
  "priority": "MELLEM"
}
```

**HB Brug:**
```bash
python ko_queue_manager.py add "Undersøg API" "MELLEM" "HB" "1487251822019350658" "aktieprojekt"
```

### Integration Point 2: KO → HB (Resultat Routing)

**KO Notificerer:**
- KO worker gemmer resultat i task
- KO sender notifikation til ASIS
- ASIS poster til `source_channel`

### Integration Point 3: FIWA → ASIS → KO

**FIWA via ASIS:**
```json
{
  "source": "ASIS",
  "source_channel": "1487251822019350658",
  "priority": "HOJ"  // FIWA kan bede om høj prioritet
}
```

---

## Prioriterings-System

| Prioritet | Betydning | Eksempel |
|-----------|-----------|----------|
| HOJ | Akut, deadlines | "Skal være færdig i dag" |
| MELLEM | Normal drift | HB research, daglige checks |
| LAV | Kan vente | Optimering, langsigtede |

**Sortering:**
```
HOJ → MELLEM → LAV
(alfabetisk + timestamp)
```

---

## Fordele ved Bridge Arkitekturen

| Feature | HB alene | HB+KO Bridge |
|---------|----------|---------------|
| Per-projekt autonomi | ✅ | ✅ |
| WAL logging | ✅ | ✅ |
| Cross-channel tasks | ❌ | ✅ |
| Prioritering | ❌ | ✅ |
| Shared worker pool | ❌ | ✅ |
| FIWA kan eskalere | ⚠️ | ✅ |
| Resultat routing | ❌ | ✅ |

---

## Implementerings-Trin

### Trin 1: KO Queue (✓ Færdig)
- [x] ko_queue.json struktur
- [x] ko_queue_manager.py CLI
- [ ] Integration med HB

### Trin 2: HB → KO Write (Igangang)
- [ ] HB tilføjer til KO
- [ ] Task metadata (source_channel, priority)
- [ ] Dokumentation

### Trin 3: KO Worker (Efter evaluering)
- [ ] KO læser queue
- [ ] Spawner agenter
- [ ] Resultat routing

### Trin 4: ASIS Integration (Senere)
- [ ] ASIS → KO add med prioritet
- [ ] ASIS præsenterer resultater
- [ ] Channel-specific ASIS sessions

---

## Teknisk Stack

| Komponent | Teknologi |
|-----------|-----------|
| KO Queue | JSON fil (`ko_queue.json`) |
| KO Manager | Python CLI (`ko_queue_manager.py`) |
| KO Worker | Python daemon (`ko_worker.py`) |
| HB | OpenClaw cron job |
| Workers | OpenClaw sessions via `sessions_spawn` |
| Resultat | JSON + Discord message |

---

## Alternativer Overvejet

### Alternativ A: Ren HB (ingen KO)
- ✅ Simpel
- ❌ Ingen cross-channel prioritering
- ❌ FIWA kan ikke eskalere

### Alternativ B: Ren KO (ingen HB)
- ✅ Central queue
- ❌ Mister per-projekt autonomi
- ❌ Ingen WAL/projekt struktur

### Valgt: Bridge (HB + KO)
- ✅ Behøver det bedste fra begge
- ✅ Fremtidssikret
- ⚠️ Mere kompleks end hver for sig

---

## Næste Skridt

1. **Test HB → KO flow** (Tilføj opgaver fra HB)
2. **Implementer KO Worker** (Læs queue, spawn agenter)
3. **ASIS add** (FIWA kan tilføje med prioritet)
4. **Resultat routing** (Tilbage til source channel)

---

## Kontakt / Auditanse

Dokumentet er lavet til review af ekstern AI konsulent.

**Spørgsmål til Reviewer:**
1. Er prioriterings-logikken fornuftig?
2. Bør KO worker køre som separat proces eller via cron?
3. Hvordan håndterer vi fejl i worker?
4. Er JSON filen tilstrækkelig eller bør vi bruge database?

---

*Sidst opdateret: 2026-04-06*
