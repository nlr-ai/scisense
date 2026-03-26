# Ngram — Patterns: Atomic Scientific Claims with Dense Linking

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
THIS:            PATTERNS_Ngram_Scientific_Knowledge_Pipeline.md (you are here)
ALGORITHM:       ./ALGORITHM_Ngram_Scientific_Knowledge_Pipeline.md
VALIDATION:      ./VALIDATION_Ngram_Scientific_Knowledge_Pipeline.md
HEALTH:          ./HEALTH_Ngram_Scientific_Knowledge_Pipeline.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ngram_Scientific_Knowledge_Pipeline.md
SYNC:            ./SYNC_Ngram_Scientific_Knowledge_Pipeline.md

IMPL:            src/ngram/
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source files

**After modifying this doc:**
1. Update the IMPL source files to match, OR
2. Add a TODO in SYNC_*.md: "Docs updated, implementation needs: {what}"

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_*.md: "Implementation changed, docs need: {what}"

---

## THE PROBLEM

Scientific studies contain rich knowledge locked in unstructured formats (PDFs, abstracts, tables). This knowledge cannot be:
- Queried semantically ("What efficacy claims exist for pembrolizumab?")
- Connected across studies ("How does this compare to competitor results?")
- Traced to source ("Where exactly does this claim come from?")

Without structured extraction, Sophie manually re-reads papers. Hugo cannot cross-reference competitive data. Clients cannot verify claims.

---

## THE PATTERN

**Atomic Claims with Dense Linking**

Transform every scientific finding into an atomic claim node:
- **Atomic**: One assertion per claim ("31% ORR" not "the study was positive")
- **Traceable**: Every claim links to source document + location
- **Connected**: Claims link to drugs, populations, biomarkers, other claims
- **Queryable**: Graph structure enables semantic search via `graph_query`

The key insight: **claims are not text, they are graph nodes**. Text is searched; nodes are traversed. Traversal enables reasoning.

---

## BEHAVIORS SUPPORTED

- **B1: Semantic Query** — Sophie queries "efficacy claims for [drug]" and gets structured results
- **B2: Competitive Analysis** — Hugo compares claims across competitor studies
- **B3: Source Verification** — Any claim can be traced to PDF page/paragraph
- **B4: Evidence Synthesis** — Claims aggregate into evidence summaries

## BEHAVIORS PREVENTED

- **Anti-B1: Orphan Claims** — Claims without source links are rejected
- **Anti-B2: Vague Assertions** — "Study was positive" is not a valid claim
- **Anti-B3: Duplicate Knowledge** — Same finding from same source creates one claim, not many

---

## PRINCIPLES

### Principle 1: Traçabilité Absolue

Every claim must link to its source. No exceptions.

Why: SciSense's value proposition is scientific rigor. Untraceable claims are worthless — worse, they're liability.

### Principle 2: Atomicity Over Completeness

One assertion per claim. Complex findings split into multiple claims.

Why: Atomic claims can be queried, compared, contradicted individually. Compound statements cannot.

### Principle 3: Dense Over Sparse

Each claim should link to as many relevant nodes as possible: drugs, populations, biomarkers, other claims, studies.

Why: Isolated nodes are invisible. Connected nodes are discoverable. Graph value grows with edge count.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| PubMed API | URL | Fetch publication metadata and abstracts |
| ClinicalTrials.gov | URL | Fetch trial design, endpoints, results |
| PDF uploads | FILE | Parse full-text publications |
| EMA EPAR | URL | European regulatory documents |
| FDA labels | URL | US regulatory documents |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| ngram membrane | Graph storage and query via MCP tools |
| citizens/sophie | Primary consumer of claim queries |
| citizens/hugo | Uses drug/company data for competitive intel |
| citizens/lea | Pulls structured claims for visualization |

---

## INSPIRATIONS

- **Knowledge Graphs**: Wikidata, Google Knowledge Graph — structured, linked, queryable
- **Evidence-Based Medicine**: Cochrane systematic reviews — atomic claims with evidence levels
- **Semantic Web**: RDF triples (subject-predicate-object) — atomic assertions

---

## SCOPE

### In Scope

- Ingestion of scientific sources (PDF, APIs)
- Extraction of claims, findings, entities
- Transformation into graph nodes with links
- Registration in ngram membrane graph

### Out of Scope

- **Visualization** → see: citizens/lea
- **Strategic interpretation** → see: citizens/sophie
- **Outreach content** → see: citizens/marie
- **Storage infrastructure** → uses ngram, doesn't own it

---

## MARKERS

@ngram:TODO Define claim node schema with membrane team
@ngram:TODO Identify first 3 studies to ingest as proof of concept
@ngram:proposition Consider real-time RSS feed ingestion for competitive monitoring
