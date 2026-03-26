# Ngram — Validation: What Must Be True

```
STATUS: DRAFT
CREATED: 2025-12-27
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Ngram_Scientific_Knowledge_Pipeline.md
PATTERNS:        ./PATTERNS_Ngram_Scientific_Knowledge_Pipeline.md
BEHAVIORS:       ./BEHAVIORS_Ngram_Scientific_Knowledge_Pipeline.md
THIS:            VALIDATION_Ngram_Scientific_Knowledge_Pipeline.md (you are here)
ALGORITHM:       ./ALGORITHM_Ngram_Scientific_Knowledge_Pipeline.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ngram_Scientific_Knowledge_Pipeline.md
HEALTH:          ./HEALTH_Ngram_Scientific_Knowledge_Pipeline.md
SYNC:            ./SYNC_Ngram_Scientific_Knowledge_Pipeline.md
```

---

## PURPOSE

**Validation = what we care about being true.**

For ngram, these are the invariants that protect SciSense's core value: scientific rigor and traçabilité. If any of these fail, claims become worthless or dangerous.

---

## INVARIANTS

### V1: Claims Are Traceable

**Why we care:** SciSense's reputation depends on verifiable claims. An untraceable claim is a liability — clients cannot verify, Sophie cannot cite, Léa cannot reference.

```
MUST:   Every narrative.claim has a sourced_from link to thing.source
MUST:   The sourced_from link has a location property (page, section, table)
NEVER:  A claim exists with null or empty sourced_from
```

### V2: Claims Are Atomic

**Why we care:** Compound claims cannot be queried individually. "Study was positive" is useless; "31% ORR vs 18%" is queryable and comparable.

```
MUST:   Each claim contains exactly one assertion
MUST:   Claims with multiple findings are split with relates[part_of] links
NEVER:  A claim statement contains "and" joining distinct assertions
```

### V3: Subjects Are Unique

**Why we care:** Duplicate drug nodes fragment queries. "pembrolizumab" and "Pembrolizumab" as separate nodes means queries miss half the data.

```
MUST:   For any drug name, exactly one thing.drug node exists
MUST:   Subject resolution checks existing graph before creating
NEVER:  Two thing.drug nodes with equivalent names (case/spelling variants)
```

### V4: Evidence Level Is Assigned

**Why we care:** Phase 3 RCT carries more weight than observational data. Without evidence level, Sophie cannot synthesize properly.

```
MUST:   Every narrative.claim has evidence_level property set
MUST:   Evidence level matches study phase/design
NEVER:  A claim exists with null evidence_level
```

### V5: Clusters Are Dense

**Why we care:** Orphan claims are invisible to graph traversal. Dense linking enables discovery and reasoning.

```
MUST:   Each claim has ≥3 links (contains, sourced_from, about)
MUST:   Study cluster connectivity ≥2.0 links/node
NEVER:  A claim with only contains link (orphan)
```

### V6: Sources Are Preserved

**Why we care:** Original documents may become unavailable. Source nodes must capture enough metadata to reconstruct provenance.

```
MUST:   thing.source has uri (URL or file path)
MUST:   thing.source has type (publication, trial, regulatory)
MUST:   thing.source has access_date (when retrieved)
NEVER:  A source node with null uri
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | System purpose fails | Claims worthless |
| **HIGH** | Major value lost | Queries incomplete |
| **MEDIUM** | Partial value lost | Works but degraded |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Traçabilité | CRITICAL |
| V2 | Atomicity | CRITICAL |
| V3 | Subject uniqueness | HIGH |
| V4 | Evidence hierarchy | HIGH |
| V5 | Discoverability | MEDIUM |
| V6 | Source preservation | HIGH |

---

## MARKERS

@ngram:TODO Define exact threshold for "equivalent names" in V3
@ngram:TODO Clarify if V5 connectivity should be per-claim or per-cluster
@ngram:proposition Add V7 for temporal validity (claims may expire with new evidence)
