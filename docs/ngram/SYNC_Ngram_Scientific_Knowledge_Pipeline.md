# Ngram — Sync: Current State

```
LAST_UPDATED: 2025-12-27
UPDATED_BY: Claude (architect posture)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Doc chain structure (OBJECTIVES → PATTERNS → ... → SYNC)
- Core concepts: atomic claims, traçabilité, dense linking
- Validation invariants V1-V6

**What's still being designed:**
- Claim node schema (exact fields)
- Subject resolution algorithm
- Evidence level calculation
- Related claim similarity algorithm

**What's proposed (v2+):**
- Real-time RSS feed ingestion
- Automated claim conflict detection
- LLM-assisted claim atomization

---

## CURRENT STATE

The ngram module exists as documentation only. No code has been written yet.

Full doc chain is complete:
- OBJECTIVES: Traçabilité #1, Query-able #2, Dense Connectivity #3
- PATTERNS: Atomic claims with dense linking
- BEHAVIORS: 5 behaviors (B1-B5), 3 anti-behaviors (A1-A3)
- ALGORITHM: 7-step ingestion pipeline
- VALIDATION: 6 invariants (V1-V6)
- IMPLEMENTATION: Planned code structure
- HEALTH: 4 pending checkers

Ready to begin implementation.

---

## IN PROGRESS

### Documentation Chain Creation

- **Started:** 2025-12-27
- **By:** Claude (architect)
- **Status:** Complete
- **Context:** Created full A-Z doc chain following ngram templates

---

## RECENT CHANGES

### 2025-12-27: Doc Chain Created

- **What:** Full documentation chain for ngram module
- **Why:** Establish design before writing code
- **Files:**
  - OBJECTIVES_Ngram_Scientific_Knowledge_Pipeline.md
  - PATTERNS_Ngram_Scientific_Knowledge_Pipeline.md
  - BEHAVIORS_Ngram_Scientific_Knowledge_Pipeline.md
  - ALGORITHM_Ngram_Scientific_Knowledge_Pipeline.md
  - VALIDATION_Ngram_Scientific_Knowledge_Pipeline.md
  - IMPLEMENTATION_Ngram_Scientific_Knowledge_Pipeline.md
  - HEALTH_Ngram_Scientific_Knowledge_Pipeline.md
  - SYNC_Ngram_Scientific_Knowledge_Pipeline.md
- **Insights:** Use "Subject" for drugs/populations (ngram taxonomy compliance)

---

## KNOWN ISSUES

### No Issues Yet

Module is in design phase, no code to have issues.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** Doc chain complete, ready for first implementation

**What you need to understand:**
- This module integrates with ngram membrane (not a separate MCP)
- Claims are graph nodes, not text documents
- Every claim MUST have sourced_from link (V1 is CRITICAL)

**Watch out for:**
- Use "Subject" not deprecated terms — ngram hook will warn
- Subject resolution must check existing graph first (avoid duplicates)
- Dense linking is not optional — sparse clusters are failures

**Open questions I had:**
- Which graph database? Neo4j? MemGraph? Built into membrane?
- LLM usage budget for claim statement generation?
- How to handle retracted studies?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Created complete documentation chain for ngram module. Design is solid: atomic claims with traçabilité, dense linking to existing graph, evidence hierarchy. Ready for implementation starting with pubmed_fetcher.py as proof of concept.

**Decisions made:**
- Use "Subject" terminology (taxonomy compliance)
- Pipeline architecture (not event-driven)
- Traçabilité as #1 objective (non-negotiable)

**Needs your input:**
- Graph database choice
- First 3 studies to ingest as POC
- LLM budget for claim extraction

---

## TODO

### Doc/Impl Drift

- [ ] DOCS→IMPL: All docs created, implementation is 0%

### Tests to Run

```bash
# No tests yet - module is documentation only
pytest tests/ngram/  # (when implemented)
```

### Immediate

- [ ] Create src/ngram/ directory structure
- [ ] Implement pubmed_fetcher.py (first handler)
- [ ] Define claim node schema in membrane

### Later

- [ ] Implement clinicaltrials_fetcher.py
- [ ] Implement pdf_parser.py
- [ ] Implement health checkers
- IDEA: Real-time competitive monitoring via RSS

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Confident about the design. The doc chain is comprehensive and follows ngram patterns correctly. Ready to start implementation.

**Threads I was holding:**
- Claim schema needs membrane team input
- Evidence level calculation could use LLM for edge cases
- Subject resolution might need fuzzy matching library

**Intuitions:**
- Start with PubMed because it's structured (easier than PDF)
- Batch ingestion will reveal scaling issues early
- Sophie will be the primary consumer — optimize for her queries

**What I wish I'd known at the start:**
- Certain terms are deprecated in ngram taxonomy — caused hook warnings
- Doc templates are very detailed — budget time for HEALTH especially

---

## POINTERS

| What | Where |
|------|-------|
| ngram templates | `/home/mind-protocol/ngram/.ngram/templates/` |
| Main module docs | `docs/ngram/` |
| Planned code | `src/ngram/` |
| Ingestion submodule | `docs/ngram/ingestion/` (has own PATTERNS) |
| Transformation submodule | `docs/ngram/transformation/` (has own PATTERNS) |
