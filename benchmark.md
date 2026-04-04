# 📊 Benchmark: ETF Universe vs OMXC25 (C20)

## Formål
Sammenligne ETF-universet's performance mod det danske C20 index over samme periode.

## Metode
- Startdato: 2026-01-06 (første handelsdag i 2026)
- Slutdato: 2026-04-04 (nyeste data)
- Beregn normaliseret performance (baseline = 100)

## Ticker Universe
- **Energi:** XOP, OIH, IYE, VDE, XLE
- **Olie-proxies:** USO, BNO
- **Forsvar:** ITA, PPA, XAR
- **Guld:** GLD, IAU
- **Benchmark:** ^OMXC25 (OMX Copenhagen 25)

## Kilder
- Yahoo Finance (yfinance)
- ^OMXC25 = OMX Copenhagen 25 (C20Nachfolge-Index)

## Evaluering
- Relative afkast over perioden
- Risiko-justeret afkast (hvis ATR/vol data tilgængelig)
- Korrelation med C20

## Status
**Phase:** 🟡 Analyse i gang (data indsamlet)

## Performance Data (2026-01-06 → 2026-04-04)

### ETF Universe vs C20 Benchmark

| Ticker | Start | Slut | Ændring | Kategori |
|--------|-------|------|---------|----------|
| USO | 70.22 | 137.92 | **+96.41%** | Olie-proxy |
| BNO | 28.75 | 54.12 | **+88.24%** | Olie-proxy |
| XOP | 126.99 | 177.72 | **+39.95%** | Olie-services |
| OIH | 311.68 | 399.05 | **+28.03%** | Olie-services |
| VDE | 130.88 | 168.06 | **+28.41%** | Energi |
| XLE | 46.59 | 59.25 | **+27.19%** | Energi |
| IYE | 49.48 | 62.83 | **+26.98%** | Energi |
| GLD | 408.76 | 429.41 | +5.05% | Guld |
| IAU | 83.71 | 87.94 | +5.05% | Guld |
| PPA | 165.28 | 169.68 | +2.67% | Forsvar |
| XAR | 260.22 | 259.58 | -0.24% | Forsvar |
| ITA | 226.33 | 221.91 | -1.95% | Forsvar |
| **^OMXC25** | 1826.99 | 1709.95 | **-6.41%** | C20 Benchmark |

### Konklusion
- **Olie/Energi ETF'ere:** +27% til +96% (massive outperformance)
- **Forsvar ETF'ere:** -2% til +3% (svag performance)
- **Guld ETF'ere:** +5% (begrænset upside)
- **C20 Benchmark:** -6.41% (nedadgående marked)

### Bemærkning
Data er fra perioden 2026-01-06 til 2026-04-04. Olie/energi har haft exceptionelt afkast pga globale forsyningschok. Historisk performance er ingen garanti for fremtidige resultater.

---

*Created: 2026-04-04*