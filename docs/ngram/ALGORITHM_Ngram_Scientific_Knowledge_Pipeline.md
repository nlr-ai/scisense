# Ngram — Algorithm: Study Ingestion and Claim Atomization Pipeline

```
STATUS: DRAFT
CREATED: 2025-12-27
VERIFIED: -
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Ngram_Scientific_Knowledge_Pipeline.md
BEHAVIORS:       ./BEHAVIORS_Ngram_Scientific_Knowledge_Pipeline.md
PATTERNS:        ./PATTERNS_Ngram_Scientific_Knowledge_Pipeline.md
THIS:            ALGORITHM_Ngram_Scientific_Knowledge_Pipeline.md (you are here)
VALIDATION:      ./VALIDATION_Ngram_Scientific_Knowledge_Pipeline.md
HEALTH:          ./HEALTH_Ngram_Scientific_Knowledge_Pipeline.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ngram_Scientific_Knowledge_Pipeline.md
SYNC:            ./SYNC_Ngram_Scientific_Knowledge_Pipeline.md

IMPL:            src/ngram/
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

The ingestion pipeline transforms raw scientific sources (PDFs, PubMed, ClinicalTrials.gov) into atomic, linked knowledge graph nodes. It runs in two phases: **Extraction** (source → structured data) and **Transformation** (structured data → graph nodes with dense linking).

---

## OBJECTIVES AND BEHAVIORS

| Objective | Behaviors Supported | Why This Algorithm Matters |
|-----------|---------------------|----------------------------|
| Atomic Traçabilité | B2, B5 | Every step preserves source location |
| Query-able Knowledge | B1, B4 | Output is graph nodes, not text |
| Dense Connectivity | B3, B4 | Algorithm enforces linking to existing nodes |

---

## DATA STRUCTURES

### Extraction Result

```yaml
extraction:
  source_id: "pmid:38892156"
  source_type: "publication"
  source_url: "https://pubmed.ncbi.nlm.nih.gov/38892156"

  metadata:
    title: "Pembrolizumab vs Docetaxel..."
    authors: ["Smith J", "Jones K"]
    publication_date: "2024-06"
    journal: "NEJM"
    nct_id: "NCT02578680"
    phase: "3"

  findings:
    - metric: "ORR"
      value: "31%"
      comparator_value: "18%"
      p_value: "<0.001"
      population: "ITT"
      location: "Table 2, Row 3"
```

### Claim Node

```yaml
claim:
  id: "narrative_CLAIM_{study_id}-{type}-{index}"
  node_type: "narrative"
  subtype: "claim"

  statement: "Pembrolizumab demonstrated 31% ORR vs 18% for docetaxel (p<0.001)"
  evidence_level: "phase_3_rct"
  confidence: 0.95

  links:
    - type: contains, from: space.study
    - type: sourced_from, to: thing.source
    - type: about, to: thing.drug
    - type: in_population, to: thing.population
```

---

## ALGORITHM: ingest_study()

### Step 1: Resolve Source

Identify source type and fetch/parse content.

```
INPUT: source_type, source_value

IF source_type == "pmid":
    extraction = fetch_pubmed(source_value)
ELIF source_type == "nct_id":
    extraction = fetch_clinicaltrials(source_value)
ELIF source_type == "pdf":
    extraction = parse_pdf(source_value)
ELIF source_type == "url":
    extraction = fetch_and_parse_url(source_value)

RETURN extraction with metadata, sections, tables, raw_findings
```

### Step 2: Check Existing

Query graph for duplicate study.

```
existing = graph_query("space.study WHERE nct_id = {nct_id} OR pmid = {pmid}")

IF existing:
    PROMPT user: "Study exists. Update / Skip / Version?"
    IF skip: RETURN early
    IF version: suffix study_id with version number
    IF update: proceed, will merge claims
```

### Step 3: Create Study Space

```
study_space = create_node(
    id: "space_STUDY_{nct_id or pmid}",
    node_type: "space",
    subtype: "study",
    fields: extraction.metadata
)

source_node = create_node(
    id: "thing_SOURCE_{pmid}",
    node_type: "thing",
    subtype: "source",
    uri: extraction.source_url
)

link(study_space, source_node, type: "sourced_from")
```

### Step 4: Resolve Subjects (Drugs, Populations, Biomarkers)

For each drug, population, biomarker mentioned:

```
FOR subject IN extraction.subjects:
    existing = graph_query("thing.{subject.type} WHERE name = {subject.name}")

    IF existing:
        subject_node = existing[0]
    ELSE:
        subject_node = create_node(
            id: "thing_{TYPE}_{slug(subject.name)}",
            node_type: "thing",
            subtype: subject.type,
            name: subject.name
        )

    STORE subject_node for later linking
```

### Step 5: Atomize Findings into Claims

For each finding, create atomic claim:

```
FOR finding IN extraction.findings:
    statement = compose_statement(finding)
    evidence_level = phase_to_evidence_level(extraction.metadata.phase)

    claim = create_node(
        id: "narrative_CLAIM_{study_id}-{finding.type}-{index}",
        node_type: "narrative",
        subtype: "claim",
        statement: statement,
        evidence_level: evidence_level,
        confidence: calculate_confidence(finding)
    )

    # Required links
    link(study_space, claim, type: "contains")
    link(claim, source_node, type: "sourced_from", properties: {location: finding.location})
    link(claim, drug_node, type: "about")
    link(claim, population_node, type: "in_population")

    # Optional links
    IF finding.comparator:
        link(claim, comparator_node, type: "compared_to")
    IF finding.biomarker:
        link(claim, biomarker_node, type: "relates", direction: "stratified_by")
```

### Step 6: Dense Linking

Find and link related claims:

```
related_claims = graph_query("narrative.claim WHERE about = {drug} AND study != {this_study}")

FOR related IN related_claims:
    similarity = compute_similarity(claim, related)

    IF similarity.supports:
        link(claim, related, type: "relates", direction: "supports", strength: similarity.score)
    ELIF similarity.contradicts:
        link(claim, related, type: "relates", direction: "contradicts", strength: similarity.score)
```

### Step 7: Record Moment

```
moment = create_node(
    id: "moment_INGEST_{study_id}_{timestamp}",
    node_type: "moment",
    text: "Ingested {study.title}: {claim_count} claims, {link_count} links"
)

link(actor_id, moment, type: "expresses")
link(moment, study_space, type: "about")
```

---

## KEY DECISIONS

### D1: Subject Resolution

```
IF exact name match in graph:
    Use existing node (no duplicate)
ELIF fuzzy match > 0.9:
    Prompt user: "Is {new} same as {existing}?"
ELSE:
    Create new subject node
```

### D2: Claim Atomicity

```
IF finding contains multiple assertions:
    Split into separate claims
    Link claims with relates[direction: part_of]
ELSE:
    One finding = one claim
```

### D3: Evidence Level Assignment

```
IF phase == "3" AND design == "RCT":
    evidence_level = "phase_3_rct" (0.95)
ELIF phase == "2":
    evidence_level = "phase_2_rct" (0.80)
ELIF design == "observational":
    evidence_level = "observational" (0.60)
ELSE:
    evidence_level = "other" (0.40)
```

---

## DATA FLOW

```
Source (PDF/PMID/NCT)
    ↓
[Extraction] → metadata, findings, raw_text
    ↓
[Subject Resolution] → drug, population, biomarker nodes (reuse or create)
    ↓
[Claim Atomization] → narrative.claim nodes with statement, evidence_level
    ↓
[Dense Linking] → links to subjects, source, related claims
    ↓
[Moment Recording] → moment.ingest with provenance
    ↓
Graph (queryable cluster)
```

---

## COMPLEXITY

**Time:** O(n × m) where n = findings, m = existing subjects/claims to check

**Space:** O(n) for claims created

**Bottlenecks:**
- Subject resolution queries (mitigate with caching)
- Related claim similarity (limit search to same therapeutic area)
- PDF parsing for large documents

---

## HELPER FUNCTIONS

### `phase_to_evidence_level(phase)`

**Purpose:** Convert study phase to evidence weight

**Logic:** Lookup table: Phase 3 RCT → 0.95, Phase 2 → 0.80, etc.

### `compose_statement(finding)`

**Purpose:** Generate human-readable claim statement from finding

**Logic:** Template: "{drug} demonstrated {metric} of {value} [vs {comparator_value}] [in {population}] [(p={p_value})]"

### `compute_similarity(claim_a, claim_b)`

**Purpose:** Determine if claims support or contradict

**Logic:** Compare drug, population, metric direction. Same direction = supports. Opposite direction = contradicts.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| ngram membrane | graph_query() | Existing nodes |
| ngram membrane | create_node() | New node ID |
| ngram membrane | link() | Link created |
| PubMed API | fetch_pubmed() | Extraction result |
| ClinicalTrials.gov API | fetch_clinicaltrials() | Extraction result |

---

## MARKERS

@ngram:TODO Define exact similarity algorithm for claim comparison
@ngram:TODO Implement fuzzy subject matching threshold tuning
@ngram:proposition Consider LLM-assisted claim statement generation for complex findings
@ngram:escalation Need decision: how to handle retracted studies?
