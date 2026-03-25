# S2b: A Standardized Protocol for Measuring Visual Comprehension of Scientific Graphical Abstracts

**Authors:** Aurore Inchauspé ¹ ², Nicolas Lester Reynolds ³

¹ SciSense, Lyon, France
² Université Claude Bernard Lyon 1, Lyon, France (PhD Virology, 2018)
³ Mind Protocol, Lyon, France

**Corresponding author:** Aurore Inchauspé (aurore@scisense.fr)

**Author note:** AI is a virologist (PhD, Université Claude Bernard Lyon 1, 2018; publications in mBio and Scientific Reports on HBV/CRISPR) with 5 years of medical affairs and scientific communication experience (Boiron Laboratories, 2020-2025), now founder of SciSense, a scientific communication consultancy. NLR designed and built the S2b platform and scoring engine within the Mind Protocol framework.

**Target journal:** PLOS ONE
**Format:** IMRaD, no strict word limit
**Status:** DRAFT — Introduction + Methods skeleton

**AI Disclosure (ICMJE 2026-compliant):**

The following AI-assisted technologies were used in the preparation of this manuscript and the development of the S2b protocol:

- **Claude (Anthropic)** was used for literature synthesis, mathematical model formalization, and manuscript drafting under the supervision of NLR. All AI-generated content was critically reviewed, edited, and validated by the human authors.
- **Sentence-transformers (paraphrase-multilingual-mpnet-base-v2)** is used in the S2b scoring pipeline for embedding-based semantic similarity computation.
- **SpeechRecognition API / Whisper (OpenAI)** is used for voice-to-text transcription in the bimodal input protocol.

The authors take full responsibility for the accuracy, integrity, and originality of this work. AI tools were not listed as authors in accordance with ICMJE 2026 recommendations.

**Acknowledgments:**

The S2b platform was implemented by Silas (AI citizen, Mind Protocol) under the direction of NLR. Literature analysis and mathematical modeling were developed with Marco (AI citizen, Mind Protocol) under the direction of NLR. The authors thank the Mind Protocol team for infrastructure support and the initial cohort of testers for their participation. The S2b source code is available at github.com/mind-protocol/scisense-s2b (Apache 2.0).

---

## Abstract

[Written last, after Results. ~250 words. Placeholder.]

---

## Introduction

Graphical Abstracts (GAs) have become a standard feature of scientific publishing. Major publishers including Elsevier, MDPI, Cell Press, and the Lancet group now encourage or require authors to submit visual summaries alongside their manuscripts [1]. The rationale is intuitive: a well-designed visual summary should communicate key findings faster and to broader audiences than a text abstract alone. The proliferation of GAs has been further accelerated by social media dissemination, where image-bearing posts consistently outperform text-only posts in engagement metrics [2-6].

The engagement effect is well documented. Ibrahim et al. found that tweets containing visual abstracts generated 7.7 times more impressions and 8.4 times more retweets than text-only tweets for the same articles [2]. Oska et al. reported a five-fold increase in engagement for visual abstracts compared to text [3]. Chapman et al. observed a 57% increase in professional engagement [4]. Across six experimental studies using crossover or randomized designs, the direction of the effect is unanimous: GAs increase visibility [2-6].

However, visibility is not comprehension. Three independent lines of evidence suggest that the engagement gains documented above do not translate into improved understanding of the underlying science.

First, Bredbenner and Simon directly compared four summary formats — video abstracts, plain language summaries, graphical abstracts, and published abstracts — on measured comprehension in a sample of 538 participants [7]. Graphical abstracts ranked third out of four, outperforming only published abstracts. Critically, the authors found no correlation between format preference and comprehension: participants preferred formats that did not help them understand the content. This preference-performance dissociation is the most consequential finding for the field.

Second, the engagement-impact dissociation is quantifiable at the article level. Bennett and Slattery analyzed 562 articles and found that while GAs nearly doubled Altmetric scores (IRR = 1.89, P = .003), they had no detectable effect on citations (IRR = 0.97, P = .829) [8]. Zong, Huang, and Deng confirmed via propensity score matching that GAs increase abstract clicks but confer no advantage for full-text views or citations [9]. The implication is stark: GAs make articles more visible but not more read.

Third, the visual format may actively distort the science it purports to communicate. Vorland et al. audited 253 visual abstracts of randomized controlled trials and found high rates of spin — defined as reporting practices that could distort the interpretation of results — compared to their corresponding text abstracts [10]. Visual compression can amplify rather than clarify distortion, particularly when visual properties such as area or color saturation are used to encode effect sizes or evidence strength without regard for perceptual accuracy.

This last point connects to a deeper problem: the absence of any established framework for mapping scientific evidence onto visual properties. The GRADE system provides the only experimentally validated visual encoding of evidence certainty, using filled circles (⊕⊕⊕⊕ to ⊕⊖⊖⊖) to represent four levels of confidence [11]. Akl et al. demonstrated that these symbols yielded 74% correct comprehension compared to 14% for numerical representations (P < .001) [12]. Rosenbaum et al. showed that Cochrane Summary of Findings tables with GRADE symbols achieved 93% comprehension versus 44% without (P = .003) [13]. Yet the GRADE visual system uses a single perceptual channel (fill proportion) in a single format (tabular), with only four levels of granularity. It has never been tested in the narrative visual formats — flowcharts, infographics, graphical abstracts — that dominate modern scientific communication.

Meanwhile, the perceptual science needed for such a framework exists but remains unapplied to evidence communication. Cleveland and McGill established the hierarchy of perceptual accuracy for encoding quantitative data, demonstrating that position on a common scale is decoded most accurately, followed by length, angle, area, and color saturation [14, 15]. Stevens' power law predicts that perceived area scales sublinearly with physical area (β ≈ 0.7), meaning that a 10-fold difference in evidence volume encoded as visual area will be perceived as approximately 5-fold [16]. MacEachren et al. showed that luminance, not saturation, is the intuitive channel for encoding uncertainty — a finding that directly contradicts common design practice [17]. Kinkeldey, MacEachren, and Schiewe explicitly recommended against using saturation to represent uncertainty [18]. Garcia-Retamero and Cokely demonstrated across 36 publications and 27,885 participants that transparent visual aids using natural frequencies improve risk comprehension robustly across diverse populations [19].

None of these principles has been systematically applied to the design of graphical abstracts. And — more critically for the present work — no standardized protocol exists to measure whether a given GA successfully transfers evidence hierarchy to its intended audience.

Existing evaluation of GAs relies almost exclusively on engagement metrics: impressions, retweets, Altmetric scores, click-through rates. As demonstrated above, these metrics measure visibility, not comprehension. No study has measured whether a reader who views a GA for five seconds — the typical dwell time during mobile feed scrolling [20] — can correctly identify the evidence hierarchy it encodes. No benchmark exists against which GAs from different domains, publishers, or design tools can be compared. No dataset stratifies comprehension by reader profile (clinical expertise, data literacy, color vision).

In this paper, we present S2b (Standardized Second-look Benchmark), the first protocol for measuring visual comprehension of scientific GAs under ecologically valid conditions. The protocol combines: (a) embedding-based semantic scoring of free recall, enabling automated assessment without keyword dependency; (b) four-alternative forced choice measurement of evidence hierarchy perception, benchmarked against the 74% comprehension rate of GRADE symbols [12]; (c) ecologically valid feed simulation with inertial scroll physics, platform-specific chrome, and heterogeneous content mix; (d) bimodal input (voice and text) with semantic filtering to address the production bottleneck in written recall [21]; and (e) stratified profiling across clinical expertise and data literacy dimensions. The protocol is domain-agnostic — the same metrics apply to GAs in medicine, computer science, economics, or climate science. The scoring pipeline and test platform are publicly available as open-source software (Apache 2.0) at github.com/mind-protocol/scisense-s2b.

---

## Methods

[Condensed from S2b_Mathematics.md. Target: ~2500 words. Structure below.]

### 2.1 Study Design

Cross-sectional diagnostic accuracy study. Each participant views one or more GAs under controlled exposure conditions and completes a three-question assessment. Two exposure modes are supported: spotlight (isolated GA, fixed 5-second exposure) and stream (GA embedded in a simulated social media feed with auto-scroll). The study follows STARD reporting guidelines for diagnostic accuracy studies [22].

### 2.2 Participants and Profiling

[Inclusion/exclusion criteria. Profiling matrix: Clinical Expertise × Data Literacy, 4 quadrants. Color vision. GRADE familiarity. Consent and ethics.]

### 2.3 Stimuli

[GA library: domains, VEC vs control pairs, metadata structure. Stimulus triplet (frame, text, image). Exposure conditions: nude, title-only, feed LinkedIn, feed Twitter, TOC journal. Distractors: types, content mix simulation, ecological validity.]

### 2.4 Exposure Protocol

[Spotlight mode: 5-second fixed exposure, brief, countdown. Stream mode: inertial flick scroll (v₀ = avgItemHeight/25, γ = 0.96), phone frame on desktop (390×844, DPR 3), seed-based reproducible sequences, IntersectionObserver dwell time measurement, exposure validation (±500ms tolerance). Screen resolution capture.]

### 2.5 Outcome Measures

#### 2.5.1 Primary Outcome: Evidence Hierarchy Perception (S9b)

[4AFC, correct = product with strongest evidence, chance = 25%, binary scoring. Benchmark: ≥80% to exceed GRADE's 74%. Aggregation: Taux_S9b = Σ S9b(i) / N.]

#### 2.5.2 Secondary Outcome: Semantic Recall (S9a)

[Free recall, embedding-based scoring (paraphrase-multilingual-mpnet-base-v2, 768d), cosine similarity, threshold θ calibrated by ROC on annotated subset. Voice input option with semantic filtering of meta-talk (θ_filter = 0.15). Justification of voice vs text: production bottleneck (Levelt 1989, Grabowski 2008).]

#### 2.5.3 Secondary Outcome: Actionability (S9c)

[3-level ordinal: yes/need more info/no. Scoring: 1/0.5/0.]

#### 2.5.4 Saliency (S10, stream mode only)

[Post-flux 3AFC recognition. Chance = 0.33. Threshold > 0.70. Coupling: S10 × S9b as complete chain metric.]

### 2.6 Temporal Metrics

[RT₂ (log-normal, median). First keystroke / first utterance latency. Production duration. Validation delay. Word count.]

### 2.7 Statistical Analysis

#### 2.7.1 Sample Size

[McNemar for paired A/B: N ≈ 30 for Δ = 0.30. Chi² for quadrants: N ≈ 80 (20/cell) for w = 0.3 at 80% power.]

#### 2.7.2 Primary Analysis

[Taux_S9b with 95% CI. McNemar test for VEC vs control. Δ_S9b with 95% CI.]

#### 2.7.3 Exploratory Analyses

[Chi² across profiling quadrants. Logistic regression: logit(S9b) = β₀ + β₁·clinical + β₂·literacy + β₃·grade + β₄·color_vision + β₅·ga_version + β₆·log(latency) + β₇·input_mode + β₈·dwell_ms + β₉·screen_dpr. Five pre-registered hypotheses H1-H5.]

### 2.8 Software and Data Availability

[Open-source platform (Apache 2.0, github.com/mind-protocol/scisense-s2b). Dependencies: FastAPI, sentence-transformers, SQLite. Anonymized dataset deposited on Zenodo/OSF upon publication. CITATION.cff for reproducibility.]

---

## Results

[Requires data. Placeholder structure:]

### 3.1 Participant Characteristics
### 3.2 Evidence Hierarchy Perception (S9b)
### 3.3 Semantic Recall (S9a)
### 3.4 Saliency in Feed Simulation (S10)
### 3.5 Temporal Dynamics
### 3.6 Profiling and Stratification
### 3.7 Voice vs Text Input

---

## Discussion

[Placeholder structure:]

### 4.1 Principal Findings
### 4.2 Comparison with Prior Work

[Bredbenner 2019: our protocol measures comprehension directly, addressing the gap they identified. Akl 2007: our S9b benchmark (80%) is calibrated against their 74% for GRADE symbols. Vorland 2024: our Δ_spoiler metric directly quantifies visual spin. Bennett & Slattery 2023: S10 provides the first controlled measure of attention capture, replacing altmetric proxies.]

### 4.3 Strengths and Limitations

[Strengths: automated scoring, ecological validity, domain-agnostic, open-source. Limitations: modest N in pilot, no eye-tracking, STT filtering for voice, self-selected online sample, single GA domain in initial validation.]

### 4.4 Implications for Practice

[For GA designers: S9b as quality metric. For publishers: S2b certification. For researchers: benchmark for visual communication quality. For the field: shift from engagement to comprehension as the standard of evaluation.]

---

## References

1. Pferschy-Wenzig EM et al. (2016). Does a graphical abstract bring more visibility? *Molecules* 21(9):1247.
2. Ibrahim AM et al. (2017). Visual abstracts to disseminate research on social media. *Ann Surg* 266(6):e46-e48.
3. Oska S, Lerma E, Topf J. (2020). A picture is worth a thousand views. *JMIR* 22(12):e22327.
4. Chapman SJ et al. (2019). Randomized controlled trial of plain English and visual abstracts. *BJS* 106(12):1611-1616.
5. Hoffberg AS et al. (2020). Beyond journals — visual abstracts promote wider dissemination. *Front Res Metr Anal* 5:564193.
6. Trueger NS et al. (2023). RCT visual abstract display and social media–driven website traffic. *JAMA Network Open*.
7. Bredbenner K, Simon SM. (2019). Video abstracts and plain language summaries are more effective than graphical abstracts and published abstracts. *PLOS ONE* 14(11):e0224697.
8. Bennett H, Slattery F. (2023). Graphical abstracts increase Altmetric attention scores but not citations. *Scientometrics* 128:3793-3804.
9. Zong Q, Huang Z, Deng Z. (2023). Effect of graphical abstracts on usage and citations. *Learned Publishing* 36(2):266-274.
10. Vorland CJ et al. (2024). Visual abstracts of RCTs: inadequate reporting and high rates of spin. *J Clin Epidemiol*.
11. Schünemann HJ et al. (2003). Letters, numbers, symbols and words: communicating grades of evidence. *CMAJ* 169(7):677-680.
12. Akl EA et al. (2007). Symbols were superior to numbers for presenting strength of recommendations. *J Clin Epidemiol* 60(12):1263-1268.
13. Rosenbaum SE et al. (2010). Summary-of-findings tables in Cochrane reviews improved clinical decision-making. *J Clin Epidemiol* 63(6):620-626.
14. Cleveland WS, McGill R. (1984). Graphical perception: theory, experimentation, and application to the development of graphical methods. *J Am Stat Assoc* 79(387):531-554.
15. Cleveland WS, McGill R. (1985). Graphical perception and graphical methods for analyzing scientific data. *Science* 229(4716):828-833.
16. Stevens SS. (1957). On the psychophysical law. *Psychological Review* 64(3):153-181.
17. MacEachren AM et al. (2012). Visual semiotics and uncertainty visualization: an empirical study. *IEEE Trans Vis Comput Graph* 18(12):2496-2505.
18. Kinkeldey C, MacEachren AM, Schiewe J. (2017). How to assess visual communication of uncertainty? A systematic review of geospatial uncertainty visualization user studies. *Cartogr J* 54(1):1-29.
19. Garcia-Retamero R, Cokely ET. (2017). Designing visual aids that promote risk literacy: a systematic review. *Human Factors* 59(4):582-627.
20. Liu Y et al. (2020). Understanding scrolling behavior on mobile devices. *Int J Hum-Comput Stud* 143:102482.
21. Grabowski J. (2008). The internal structure of university students' keyboard skills. *Written Language & Literacy* 11(1):1-24.
22. Bossuyt PM et al. (2015). STARD 2015: an updated list of essential items for reporting diagnostic accuracy studies. *BMJ* 351:h5527.

---

## Figures (planned)

**Figure 1.** S2b protocol flow diagram. (A) Spotlight mode: brief → 5-second exposure → Q1-Q3. (B) Stream mode: feed simulation with inertial scroll → post-flux selection → Q1-Q3.

**Figure 2.** S9b (evidence hierarchy perception) by exposure condition and GA version (VEC vs control). Error bars: 95% CI.

**Figure 3.** Saliency-comprehension coupling. Scatter plot of S10 (x-axis) vs S9b (y-axis) for each GA tested in stream mode. Quadrants defined by S10 = 0.70 and S9b = 0.80 thresholds.

**Figure 4.** Profiling matrix. Heatmap of S9b by clinical expertise (rows) × data literacy (columns). Cell size proportional to N.

**Figure 5.** Temporal dynamics. Distribution of RT₂ (reaction time for Q2) by S9b outcome (correct vs incorrect). Violin plot with median marked.

---

*Draft initiated: 25 March 2026*
*Next: crash test data → Results → Discussion → Abstract → Submit*
