# Ngram — Health: Verification Mechanics and Coverage

```
STATUS: DRAFT
CREATED: 2025-12-27
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the ngram module's claim ingestion pipeline. It verifies that ingested claims meet traçabilité and connectivity requirements at runtime.

**Why it exists:** Tests cannot catch drift in claim quality over time. Health checks monitor that every claim maintains required links and evidence levels across real data.

**Boundaries:** This file verifies claim structure and connectivity. It does not verify scientific accuracy (that's Sophie's review).

---

## WHY THIS PATTERN

HEALTH is separate from tests because claim quality is emergent — it depends on source quality, extraction accuracy, and graph state at ingestion time. Docking-based checks observe real claims as they enter the graph without modifying ingestion code.

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Ngram_Scientific_Knowledge_Pipeline.md
PATTERNS:        ./PATTERNS_Ngram_Scientific_Knowledge_Pipeline.md
BEHAVIORS:       ./BEHAVIORS_Ngram_Scientific_Knowledge_Pipeline.md
ALGORITHM:       ./ALGORITHM_Ngram_Scientific_Knowledge_Pipeline.md
VALIDATION:      ./VALIDATION_Ngram_Scientific_Knowledge_Pipeline.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ngram_Scientific_Knowledge_Pipeline.md
THIS:            HEALTH_Ngram_Scientific_Knowledge_Pipeline.md (you are here)
SYNC:            ./SYNC_Ngram_Scientific_Knowledge_Pipeline.md

IMPL:            src/ngram/health/
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes.

---

## FLOWS ANALYSIS

```yaml
flows_analysis:
  - flow_id: ingest_study
    purpose: Transform source into queryable claims. If fails, claims are untraceable or orphaned.
    triggers:
      - type: manual
        source: MCP tool call
        notes: User or agent calls ingest_study()
    frequency:
      expected_rate: 1-5/day
      peak_rate: 20/day (batch ingestion)
      burst_behavior: Sequential processing, no queue
    risks:
      - V1: Claims without sourced_from link
      - V5: Orphan claims with low connectivity
    notes: Each study creates 5-50 claims, 50-200 links
```

---

## HEALTH INDICATORS SELECTED

## OBJECTIVES COVERAGE

| Objective | Indicators | Why These Signals Matter |
|-----------|------------|--------------------------|
| Atomic Traçabilité | claim_has_source | Every claim must be verifiable |
| Dense Connectivity | cluster_connectivity | Orphan claims are invisible |
| Query-able Knowledge | evidence_level_present | Sophie needs evidence hierarchy |

```yaml
health_indicators:
  - name: claim_has_source
    flow_id: ingest_study
    priority: high
    rationale: Untraceable claims damage SciSense reputation

  - name: cluster_connectivity
    flow_id: ingest_study
    priority: medium
    rationale: Low connectivity means claims are undiscoverable

  - name: evidence_level_present
    flow_id: ingest_study
    priority: high
    rationale: Evidence hierarchy is core to synthesis
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: docs/ngram/SYNC_Ngram_Scientific_Knowledge_Pipeline.md
  result:
    representation: enum
    value: PENDING
    updated_at: 2025-12-27
    source: manual (no code yet)
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: claim_traçabilité_checker
    purpose: Verify V1 - every claim has sourced_from link
    status: pending
    priority: high

  - name: cluster_density_checker
    purpose: Verify V5 - cluster connectivity ≥2.0 links/node
    status: pending
    priority: medium

  - name: evidence_level_checker
    purpose: Verify V4 - every claim has evidence_level set
    status: pending
    priority: high

  - name: subject_uniqueness_checker
    purpose: Verify V3 - no duplicate drug/population nodes
    status: pending
    priority: high
```

---

## INDICATOR: claim_has_source

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: claim_has_source
  client_value: Every claim Sophie uses can be verified against original source
  validation:
    - validation_id: V1
      criteria: Every narrative.claim has sourced_from link with location property
```

### HEALTH REPRESENTATION

```yaml
representation:
  selected:
    - binary
    - float_0_1
  semantics:
    binary: 1 = all claims have source, 0 = any claim missing source
    float_0_1: (claims with source) / (total claims)
  aggregation:
    method: min (any failure = 0)
    display: binary
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: dock_claim_created
    method: transformation.claim_atomizer.atomize_findings
    location: src/ngram/transformation/claim_atomizer.py:TBD
  output:
    id: dock_cluster_complete
    method: transformation.dense_linker.link_related_claims
    location: src/ngram/transformation/dense_linker.py:TBD
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Query all claims created in last ingestion, verify each has sourced_from link
  steps:
    - Get all narrative.claim nodes in cluster
    - For each claim, check exists(link WHERE type=sourced_from)
    - If any missing, flag as ERROR
  data_required: Claim nodes, link structure
  failure_mode: Claim exists without sourced_from link
```

### INDICATOR

```yaml
indicator:
  error:
    - name: missing_source_link
      linked_validation: [V1]
      meaning: Claim created without traçabilité
      default_action: stop ingestion, escalate
  warning:
    - name: source_location_missing
      linked_validation: [V1]
      meaning: Source link exists but location property empty
      default_action: warn, add TODO
```

### THROTTLING STRATEGY

```yaml
throttling:
  trigger: after each ingest_study() call
  max_frequency: 1/ingestion
  burst_limit: N/A (per-ingestion)
  backoff: N/A
```

---

## INDICATOR: cluster_connectivity

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: cluster_connectivity
  client_value: Claims are discoverable via graph traversal
  validation:
    - validation_id: V5
      criteria: Cluster connectivity ≥2.0 links/node
```

### HEALTH REPRESENTATION

```yaml
representation:
  selected:
    - float_0_1
    - enum
  semantics:
    float_0_1: (actual links/node) / 5.0, capped at 1.0
    enum: EXCELLENT (≥3.5), GOOD (≥2.0), SPARSE (<2.0)
  aggregation:
    method: min
    display: enum
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Count links and nodes in cluster, compute ratio
  steps:
    - Count all nodes in cluster
    - Count all links in cluster
    - Compute ratio = links / nodes
    - Compare against threshold 2.0
  data_required: Cluster node/link counts
  failure_mode: Ratio < 2.0
```

---

## HOW TO RUN

```bash
# Run all health checks for ngram (when implemented)
python -m ngram.health.run_all

# Run specific checker
python -m ngram.health.claim_traçabilité_checker
```

---

## KNOWN GAPS

@ngram:TODO Implement claim_traçabilité_checker
@ngram:TODO Implement cluster_density_checker
@ngram:TODO Implement evidence_level_checker
@ngram:TODO Implement subject_uniqueness_checker

---

## MARKERS

@ngram:TODO No checkers implemented yet - all pending
@ngram:proposition Add real-time health dashboard for Sophie
