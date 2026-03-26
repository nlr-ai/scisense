# Ngram — Implementation: Code Architecture and Structure

```
STATUS: DRAFT
CREATED: 2025-12-27
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Ngram_Scientific_Knowledge_Pipeline.md
BEHAVIORS:       ./BEHAVIORS_Ngram_Scientific_Knowledge_Pipeline.md
PATTERNS:        ./PATTERNS_Ngram_Scientific_Knowledge_Pipeline.md
ALGORITHM:       ./ALGORITHM_Ngram_Scientific_Knowledge_Pipeline.md
VALIDATION:      ./VALIDATION_Ngram_Scientific_Knowledge_Pipeline.md
THIS:            IMPLEMENTATION_Ngram_Scientific_Knowledge_Pipeline.md (you are here)
HEALTH:          ./HEALTH_Ngram_Scientific_Knowledge_Pipeline.md
SYNC:            ./SYNC_Ngram_Scientific_Knowledge_Pipeline.md

IMPL:            src/ngram/
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
src/ngram/
├── __init__.py                              # Exports main functions
├── ingestion/
│   ├── __init__.py
│   ├── pubmed_fetcher.py                    # Fetch from PubMed API
│   ├── clinicaltrials_fetcher.py            # Fetch from CT.gov API
│   ├── pdf_parser.py                        # Parse PDF documents
│   └── extraction_schema.py                 # Extraction data structures
├── transformation/
│   ├── __init__.py
│   ├── claim_atomizer.py                    # Split findings into claims
│   ├── subject_resolver.py                  # Find/create drugs, populations
│   ├── dense_linker.py                      # Connect claims to existing graph
│   └── evidence_calculator.py               # Assign evidence levels
└── membrane_tools/
    ├── __init__.py
    └── register_ingest_tools.py             # Register tools with ngram MCP
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `ingestion/pubmed_fetcher.py` | Fetch PubMed data | `fetch_pubmed()` | ~100 | PLANNED |
| `ingestion/clinicaltrials_fetcher.py` | Fetch CT.gov data | `fetch_clinicaltrials()` | ~100 | PLANNED |
| `ingestion/pdf_parser.py` | Parse PDF documents | `parse_pdf()` | ~200 | PLANNED |
| `transformation/claim_atomizer.py` | Create atomic claims | `atomize_findings()` | ~150 | PLANNED |
| `transformation/subject_resolver.py` | Resolve drugs/populations | `resolve_subject()` | ~100 | PLANNED |
| `transformation/dense_linker.py` | Link to existing graph | `link_related_claims()` | ~150 | PLANNED |

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Pipeline

**Why this pattern:** Data flows linearly: Source → Extraction → Transformation → Graph. Each stage is independent and testable.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Strategy | `ingestion/*_fetcher.py` | Different fetch strategies per source type |
| Factory | `subject_resolver.py` | Create or retrieve subject nodes |
| Visitor | `claim_atomizer.py` | Process different finding types uniformly |

### Anti-Patterns to Avoid

- **God Object**: Don't let `claim_atomizer.py` handle linking too
- **Premature Abstraction**: Start with concrete fetchers, abstract later if needed

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Ingestion | Fetching, parsing | Graph operations | `Extraction` schema |
| Transformation | Claim creation, linking | Source fetching | membrane tools |

---

## SCHEMA

### Extraction

```yaml
Extraction:
  required:
    - source_id: string           # "pmid:38892156"
    - source_type: enum           # publication, trial, regulatory
    - metadata: dict              # title, authors, date, phase
  optional:
    - findings: list[Finding]     # extracted results
    - sections: list[Section]     # document structure
  constraints:
    - source_id must be unique
```

### Claim

```yaml
Claim:
  required:
    - statement: string           # atomic assertion
    - evidence_level: enum        # phase_3_rct, observational, etc.
  optional:
    - confidence: float           # 0.0-1.0
    - caveats: list[string]       # limitations
  relationships:
    - sourced_from: thing.source
    - about: thing.drug
    - in_population: thing.population
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `ingest_study()` | `membrane_tools/register_ingest_tools.py` | MCP tool call |
| `fetch_pubmed()` | `ingestion/pubmed_fetcher.py` | `ingest_study()` |
| `atomize_findings()` | `transformation/claim_atomizer.py` | `ingest_study()` |

---

## DATA FLOW AND DOCKING

### Ingest Study Flow: Source to Graph

Explain what this flow covers: Complete ingestion of a scientific study from source to graph nodes.

```yaml
flow:
  name: ingest_study
  purpose: Transform scientific source into queryable knowledge graph
  scope: PDF/API → Extraction → Claims → Graph nodes with links
  steps:
    - id: fetch
      description: Retrieve data from source
      file: ingestion/{type}_fetcher.py
      function: fetch_{type}()
      input: source_id (string)
      output: Extraction
      trigger: MCP tool call
      side_effects: none

    - id: resolve_subjects
      description: Find or create drug/population nodes
      file: transformation/subject_resolver.py
      function: resolve_subjects()
      input: Extraction.mentions
      output: dict[name -> node_id]
      trigger: step: fetch
      side_effects: may create graph nodes

    - id: atomize
      description: Create claim nodes from findings
      file: transformation/claim_atomizer.py
      function: atomize_findings()
      input: Extraction.findings + subject_ids
      output: list[Claim nodes]
      trigger: step: resolve_subjects
      side_effects: creates graph nodes

    - id: link
      description: Connect claims to existing knowledge
      file: transformation/dense_linker.py
      function: link_related_claims()
      input: Claim nodes
      output: list[links created]
      trigger: step: atomize
      side_effects: creates graph links

  docking_points:
    guidance:
      include_when: Data transforms, graph writes, validation points
      omit_when: Internal processing, temporary structures
    available:
      - id: dock_extraction_output
        type: custom
        direction: output
        file: ingestion/{type}_fetcher.py
        function: fetch_{type}()
        payload: Extraction
        notes: Validate extraction completeness

      - id: dock_claim_created
        type: graph_ops
        direction: output
        file: transformation/claim_atomizer.py
        function: atomize_findings()
        payload: Claim node
        notes: Validate claim has required links

      - id: dock_cluster_complete
        type: graph_ops
        direction: output
        file: transformation/dense_linker.py
        function: link_related_claims()
        payload: Cluster summary
        notes: Validate connectivity metrics

    health_recommended:
      - dock_id: dock_claim_created
        reason: Every claim must have sourced_from link (V1)
      - dock_id: dock_cluster_complete
        reason: Cluster must have ≥2.0 links/node (V5)
```

---

## LOGIC CHAINS

### LC1: Claim Creation

**Purpose:** Transform a finding into a traceable claim node

```
finding (from extraction)
  → compose_statement()          # Create human-readable assertion
    → calculate_evidence_level() # Based on study phase
      → create_node(claim)       # In graph
        → link(sourced_from)     # To source
          → link(about)          # To drug
            → claim node
```

### LC2: Subject Resolution

**Purpose:** Ensure no duplicate drug/population nodes

```
subject_name (from finding)
  → graph_query(thing.drug WHERE name = X)
    → IF found: return existing node
    → ELSE: create_node(thing.drug)
      → return new node
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
membrane_tools/
    └── imports → ingestion/
    └── imports → transformation/

transformation/
    └── imports → ingestion/extraction_schema
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `httpx` | Async HTTP client | `pubmed_fetcher.py`, `clinicaltrials_fetcher.py` |
| `pdfplumber` | PDF parsing | `pdf_parser.py` |
| `pydantic` | Schema validation | `extraction_schema.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Graph nodes | ngram membrane | Global | Persistent |
| Extraction cache | In-memory | Session | Per-ingestion |

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Register MCP tools with membrane
2. Load existing subject cache (optional)
3. Ready for ingest calls
```

### Request Cycle

```
1. MCP tool call: ingest_study(source_type, source_value)
2. Fetch/parse source
3. Resolve subjects
4. Atomize findings
5. Link to existing graph
6. Record moment
7. Return cluster summary
```

---

## BIDIRECTIONAL LINKS

### Code → Docs

| File | Line | Reference |
|------|------|-----------|
| `src/ngram/__init__.py` | 1 | `# DOCS: docs/ngram/PATTERNS_Ngram_Scientific_Knowledge_Pipeline.md` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM step 1 | `ingestion/*_fetcher.py` |
| ALGORITHM step 4 | `transformation/subject_resolver.py` |
| ALGORITHM step 5 | `transformation/claim_atomizer.py` |
| BEHAVIOR B2 | `transformation/claim_atomizer.py:link_sourced_from()` |
| VALIDATION V1 | TBD (test) |

---

## MARKERS

@ngram:TODO Create initial file structure (currently empty)
@ngram:TODO Implement pubmed_fetcher.py first as proof of concept
@ngram:proposition Consider caching subject lookups for batch ingestion
