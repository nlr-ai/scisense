# Ngram — Behaviors: Observable Effects of Scientific Knowledge Ingestion

```
STATUS: DRAFT
CREATED: 2025-12-27
VERIFIED: -
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Ngram_Scientific_Knowledge_Pipeline.md
THIS:            BEHAVIORS_Ngram_Scientific_Knowledge_Pipeline.md (you are here)
PATTERNS:        ./PATTERNS_Ngram_Scientific_Knowledge_Pipeline.md
ALGORITHM:       ./ALGORITHM_Ngram_Scientific_Knowledge_Pipeline.md
VALIDATION:      ./VALIDATION_Ngram_Scientific_Knowledge_Pipeline.md
HEALTH:          ./HEALTH_Ngram_Scientific_Knowledge_Pipeline.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ngram_Scientific_Knowledge_Pipeline.md
SYNC:            ./SYNC_Ngram_Scientific_Knowledge_Pipeline.md

IMPL:            src/ngram/
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Study Ingestion Creates Queryable Cluster

**Why:** Raw PDFs/APIs are useless until transformed into queryable graph nodes. This behavior ensures every ingested study becomes discoverable.

```
GIVEN:  A scientific study source (PMID, NCT ID, or PDF)
WHEN:   Ingestion protocol runs
THEN:   A space.study node is created in the graph
AND:    All extracted claims are linked to this study space
AND:    The study is queryable via graph_query("studies about [topic]")
```

### B2: Claims Trace to Source Location

**Why:** Traçabilité is objective #1. Without source links, claims are worthless assertions.

```
GIVEN:  A claim is extracted from a study
WHEN:   The claim node is created
THEN:   It has a sourced_from link to thing.source
AND:    The source includes document location (page, section, table row)
AND:    Sophie can verify the claim against original text
```

### B3: Drugs and Populations Are Reused Not Duplicated

**Why:** If "pembrolizumab" creates a new node every time, queries fail. Existing nodes must be linked.

```
GIVEN:  A claim mentions a drug or population
WHEN:   The claim is being created
THEN:   The system queries for existing thing.drug or thing.population
AND:    If found, links to existing node
AND:    Only creates new node if not found
```

### B4: Claims Connect to Related Claims

**Why:** Isolated claims don't enable reasoning. Connected claims reveal patterns, contradictions, support.

```
GIVEN:  Multiple claims exist about the same drug
WHEN:   A new claim is ingested
THEN:   The system identifies related claims
AND:    Creates relates links with direction (supports, contradicts, elaborates)
AND:    Cluster connectivity ≥2.0 links/node
```

### B5: Evidence Level Is Assigned

**Why:** Phase 3 RCT carries more weight than case series. Sophie needs evidence hierarchy for synthesis.

```
GIVEN:  A claim is extracted from a study
WHEN:   The claim node is created
THEN:   It has evidence_level property set
AND:    Level is derived from study phase/type
AND:    Confidence score is calculated
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | Query-able Knowledge | Studies become discoverable, not buried |
| B2 | Atomic Traçabilité | Every claim verifiable |
| B3 | Dense Connectivity | No orphan nodes, reuse existing entities |
| B4 | Dense Connectivity | Claims form reasoning network |
| B5 | Query-able Knowledge | Evidence weight enables ranking |

---

## INPUTS / OUTPUTS

### Primary Function: `ingest_study()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| source_type | enum | "pmid", "nct_id", "pdf", "url" |
| source_value | string | The identifier or path |
| actor_id | string | Who is ingesting (for moment) |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| cluster | object | Created nodes and links |
| study_id | string | The space.study node ID |
| claim_count | int | Number of claims extracted |

**Side Effects:**

- Creates nodes in ngram graph via membrane
- Creates moment recording ingestion
- May update existing drug/population nodes with new links

---

## EDGE CASES

### E1: Study Already Exists

```
GIVEN:  A study with same PMID/NCT ID already exists in graph
THEN:   Protocol asks: update, skip, or create version
AND:    If update: new claims added, existing preserved
AND:    If version: new study space with version suffix
```

### E2: No Claims Extractable

```
GIVEN:  A study source that yields no parseable claims
THEN:   Study space is still created (metadata only)
AND:    Moment records "no claims extracted, needs manual review"
AND:    @ngram:TODO is added for manual processing
```

### E3: Conflicting Claims Same Study

```
GIVEN:  Same study contains contradictory assertions (subgroups differ)
THEN:   Both claims are created
AND:    They link to each other with relates[direction: contradicts]
AND:    Population context differentiates them
```

---

## ANTI-BEHAVIORS

### A1: Orphan Claims

```
GIVEN:   A claim is created
WHEN:    Processing completes
MUST NOT: Claim exists with only contains link to study
INSTEAD:  Claim must have ≥3 links (contains, sourced_from, about)
```

### A2: Duplicate Drugs

```
GIVEN:   Claim mentions "pembrolizumab"
WHEN:    thing.drug node for pembrolizumab already exists
MUST NOT: Create a second thing_DRUG_pembrolizumab node
INSTEAD:  Link claim to existing drug node
```

### A3: Untraceable Claims

```
GIVEN:   A claim is created
WHEN:    No source location is available
MUST NOT: Create claim with null sourced_from
INSTEAD:  Either find source or mark claim as @ngram:escalation for human review
```

---

## MARKERS

@ngram:TODO Define exact format for source location (page:paragraph vs section:sentence)
@ngram:TODO Clarify versioning strategy when study is re-ingested with updates
@ngram:proposition Add "confidence_override" for human-verified claims
