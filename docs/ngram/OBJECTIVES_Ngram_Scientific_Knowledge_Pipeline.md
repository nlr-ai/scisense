# OBJECTIVES — Ngram (Scientific Knowledge Pipeline)

```
STATUS: DRAFT
CREATED: 2025-12-27
VERIFIED: -
```

## PRIMARY OBJECTIVES (ranked)

1. **Atomic Traçabilité** — Every claim traces to source location. Without this, Sophie cannot verify, Léa cannot cite, clients cannot trust. This is non-negotiable.

2. **Query-able Knowledge** — Claims structured for semantic search. "What efficacy claims exist for pembrolizumab in NSCLC?" must return useful results via `graph_query`.

3. **Dense Connectivity** — Each claim links to drugs, populations, biomarkers, other claims. Isolated claims are useless; connected claims enable reasoning.

## NON-OBJECTIVES

- **Storage infrastructure** — We use ngram's graph, we don't build our own database
- **Visualization** — That's Léa's domain; we produce structured data, not charts
- **Strategic interpretation** — That's Sophie's domain; we atomize, she synthesizes
- **Real-time ingestion** — Batch processing is acceptable; we optimize for quality over speed

## TRADEOFFS (canonical decisions)

- When **completeness** conflicts with **accuracy**, choose accuracy. A missing claim is better than a wrong claim.
- When **speed** conflicts with **traçabilité**, choose traçabilité. Every claim must have source.
- We accept **manual review overhead** to preserve **evidence quality**. LLM extraction is assisted, not autonomous.

## SUCCESS SIGNALS (observable)

- Sophie can query "claims about [drug] in [population]" and get useful results
- Every claim in graph has non-null `sourced_from` link
- Cluster connectivity ≥2.0 links/node
- Hugo can find competitive intelligence via drug/company queries

@ngram:TODO Validate objectives with Aurore — confirm traçabilité is indeed #1 priority
