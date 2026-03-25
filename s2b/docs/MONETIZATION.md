# S2b Premier Regard -- Monetization Strategy

## Context

S2b is the validation layer of SciSense's Visual Evidence Compiler (VEC). It proves -- quantitatively -- that a GA transfers its information hierarchy correctly. The business model turns this proof into revenue.

**Current state (March 2026):** Platform running at localhost. 47 GA images across 15 domains. Semantic scoring operational. Flux (stream) mode live. No external users yet.

---

## 4 Revenue Streams

### 1. VEC Service (consulting, high margin)

**What:** SciSense produces or audits Graphical Abstracts for journal publishers, pharma companies, and research institutions using the VEC methodology. S2b provides the quantitative proof that the deliverable works.

**Deliverable:** GA design + S2b validation report showing Taux_S9b, speed-accuracy profile, cross-profile quadrant analysis.

**Pricing:** EUR 850+/day (SciSense tarif plancher). Retainers at EUR 4000+/month.

**Available now:** VEC methodology exists. S2b runs locally. The workflow is: client provides data -> VEC generates GA -> S2b validates -> deliver GA + validation report.

**Timeline:** Revenue-ready now (pending first client).

### 2. S2b Certification (productized service)

**What:** A standardized certification that a GA has passed S2b validation. Publishers or pharma companies submit their GAs and receive a certification score.

**Deliverable:** S2b Certification Mark: "This GA achieved Taux_S9b >= 0.80 across N participants in S2b Premier Regard testing." Includes Taux_S9b, Score_S9c, speed-accuracy breakdown, profile quadrant analysis.

**Pricing model:** Per-GA certification fee. Tiered: basic (N=20, EUR 200-500), full (N=50+, EUR 500-1500), with cross-profile stratification.

**Timeline:** Q3 2026. Requires: deployed platform (not localhost), 50+ participant pool, standardized report template.

### 3. Platform (freemium SaaS)

**What:** S2b as a self-service web platform. Researchers upload their GAs, recruit participants, and get S2b scores.

**Free tier:** Upload 1 GA, run up to 10 tests, see basic Taux_S9b and S2b composite.

**Paid tier:** Multiple GAs, A/B testing (VEC vs control), full profile quadrant analysis, S10 saillance in stream mode, export raw data.

**Pricing model:** Subscription. EUR 50-200/month for researchers, EUR 500-2000/month for publishers.

**Timeline:** Q4 2026 - Q1 2027. Requires: cloud deployment, multi-tenant DB, user authentication, participant recruitment pipeline.

### 4. Data Licensing (long-term)

**What:** Aggregated, anonymized S2b data sold to publishers, visualization researchers, and design tool companies.

**Value proposition:** The S2b dataset is the only standardized, cross-domain, cross-profile comprehension benchmark for scientific visualizations. No equivalent exists.

**Products:**
- Annual benchmark report: "State of GA Comprehension 2027" (aggregated Taux_S9b by domain, chart type, encoding channel)
- Research dataset: anonymized test results for meta-analysis
- Design guidelines: empirically validated rules for GA design (derived from S2b data)

**Pricing model:** Report subscriptions (EUR 5000-20000/year), dataset licensing (per-query or annual), consulting on top.

**Timeline:** 2027+. Requires: 1000+ tests, 10+ domains, published validation paper.

---

## Virality Flywheel

```
                  +----------------+
                  |  Participant   |
                  |  takes test    |
                  +-------+--------+
                          |
                          v
                  +-------+--------+
                  |  Sees score    |
                  |  (S2b, S10)   |
                  +-------+--------+
                          |
                          v
                  +-------+--------+
                  |  Shares score  |<--- Leaderboard (planned)
                  |  on social     |     drives competition
                  +-------+--------+
                          |
                          v
                  +-------+--------+
                  |  New users     |
                  |  discover S2b  |
                  +-------+--------+
                          |
                          v
                  +-------+--------+
                  |  More data     |
                  |  = better      |
                  |  benchmarks    |
                  +-------+--------+
                          |
                          v
                  +-------+--------+
                  |  Attracts      |
                  |  publishers    |
                  |  & pharma      |
                  +----------------+
```

### Leaderboard (planned)

A public leaderboard showing:
- Best-performing GAs by Taux_S9b (anonymized or public, author's choice)
- Cross-domain comparison: which scientific domain produces the most comprehensible GAs?
- Speed-accuracy profiles: which GAs are "fast & right"?
- S10 rankings: which GAs are scroll-stopping?

The leaderboard serves as content engine: researchers share their rankings, compete for top spots, recruit participants to improve their scores. Each shared link brings new users to the platform.

---

## Killer Metrics for Sales

### Delta_spoiler: The VEC Differentiator

```
Delta_spoiler = S9b(title_only) - S9b(nude)
```

If Delta_spoiler is high (> +0.10), the GA's title is carrying the information -- the GA is decorative. If Delta_spoiler is low (< +0.10), the GA encodes information independently of text context.

**Sales pitch:** "Your current GA relies on the title to transfer information. With VEC, the GA itself carries the message. Here's the S2b proof: Delta_spoiler dropped from 0.35 to 0.05."

This metric is not yet implemented (requires `stimulus_condition` beyond `nude`), but it is the single most compelling data point for enterprise sales.

### Delta_S9b: The A/B Proof

```
Delta_S9b = Taux_S9b(VEC) - Taux_S9b(control)
```

**Sales pitch:** "Your area-encoded GA achieves 45% correct hierarchy perception. The VEC version achieves 85%. That's a +40 point improvement, statistically significant (McNemar chi2 = 12.3, p < 0.001). Your readers are 2x more likely to understand the key finding."

This metric is operational now. Every GA in the library has both a VEC bar chart and an area-encoded control.

### S10 x S9b: The Full Chain

**Sales pitch:** "Your GA doesn't just need to be understood -- it needs to be noticed. In our simulated scroll test, your GA was selected 78% of the time (scroll-stopping validated) AND achieved 82% correct hierarchy perception. The S10 x S9b chain metric is 0.64 -- above the 0.56 threshold for demonstrated clinical impact potential."

---

## Timeline

### Available now (Q1 2026)

- S2b platform running locally
- 47 GA images, 15 domains, A/B controls for every paper
- Semantic S9a scoring (mpnet-base-v2, 768-dim)
- Flux (stream) mode with S10 saillance measurement
- Dashboard with full analytics (aggregate, quadrant, A/B delta, S10)
- Validation report generation (manual, from dashboard data)

### Q3 2026

- Cloud deployment (accessible URL)
- Standardized certification report template
- Participant recruitment pipeline (university partnerships, online panels)
- S2b certification product launch
- First paying certification clients (target: 5-10)

### Q4 2026

- Platform freemium launch
- Multi-tenant database
- User authentication + GA upload
- Leaderboard v1
- stimulus_condition implementation (title_only, then toc_sim)
- Delta_spoiler metric live

### 2027

- Social-sim condition
- Data licensing product
- Published validation paper (with S2b methodology + N=500+ dataset)
- Annual benchmark report v1
- API for programmatic GA submission + result retrieval
