# S2b — Modèle Mathématique
# De la réponse brute à la preuve quantitative

**SciSense × Mind Protocol — Mars 2026**

---

## 1. Variables Mesurées

Chaque test produit un vecteur de mesures brutes :

```
T = {
    participant_id,         -- identifiant unique (lié au profil)
    ga_id,                  -- quel GA a été montré

    -- Condition d'exposition (le contexte)
    exposure_mode,          -- 'spotlight' | 'stream'
    exposure_condition,     -- 'nude' | 'title_only' | 'toc_sim' | 'social_sim'
    stimulus_frame,         -- quel chrome autour de l'image (none | mdpi_grid | twitter_card | linkedin_card)
    stimulus_text,          -- texte accompagnant (null | titre seul | titre+auteurs | tweet complet)
    stimulus_image_width,   -- largeur effective en px (200 pour TOC, 500 pour social, 550 pour nude)

    -- Intégrité
    tab_switched,           -- bool : le participant a-t-il changé d'onglet pendant l'exposition ?
    exposure_actual_ms,     -- durée réelle d'exposition (≤5000 si tab switch)

    -- Q1 : Rappel libre
    q1_text,                -- rappel libre (string)
    q1_first_keystroke_ms,  -- temps entre apparition Q1 et première frappe (ms)
    q1_last_keystroke_ms,   -- temps entre apparition Q1 et dernière frappe (ms)
    q1_rt,                  -- temps entre apparition Q1 et soumission (ms)

    -- Q2 : Hiérarchie
    q2_choice,              -- choix hiérarchie (enum)
    q2_rt,                  -- temps entre apparition Q2 et clic (ms)

    -- Q3 : Actionnabilité
    q3_choice               -- (yes | no | need_more)
}
```

### Définition formelle du stimulus

Le GA n'existe jamais seul dans la nature. Le stimulus est un **triplet** :

```
Stimulus = (frame, text, image)
```

| Composant | Définition | Exemples |
|-----------|-----------|----------|
| `frame` | Le chrome visuel autour de l'image — la "coquille" de la plateforme | Aucun / grille TOC MDPI / card Twitter / card LinkedIn |
| `text` | Le texte accompagnant qui peut ancrer, spoiler, ou biaiser l'interprétation | Aucun / titre article / titre+auteurs / tweet 280 chars |
| `image` | Le GA à la résolution de la plateforme simulée | 200px (TOC thumbnail) / 500px (social) / 550px (nude) |

### Les 4 conditions d'exposition

| Condition | Frame | Texte | Image width | Ce qu'on isole |
|-----------|-------|-------|-------------|----------------|
| **Nude** | Aucun | Aucun | 550px | Performance pure du design — le GA seul, sans aide ni spoiler |
| **Title-only** | Minimal | Titre de l'article | 550px | Effet du titre : spoile-t-il S9b ? Le titre porte-t-il l'info à la place du GA ? |
| **TOC-sim** | Grille MDPI (6-8 thumbnails) | Titre + auteurs | 200px | Survie au downscale. Stress test P6 (mobile-first) et V7 (lisibilité 50%) |
| **Social-sim** | Card Twitter/LinkedIn | Tweet/post complet | 500px | Effet d'ancrage textuel. Le tweet biaise-t-il l'interprétation ? |

**Pourquoi ces 4 conditions :**

La condition **Nude** est le baseline. C'est le seul moyen d'isoler l'effet du *design du GA* de tout contexte. Si S9b(Nude) < 0.80, le design est cassé — pas besoin de tester les autres conditions. C'est le premier test, toujours.

La condition **Title-only** est le test de spoiler. Si S9b(Title-only) >> S9b(Nude), le titre porte l'information — le GA est décoratif, pas informatif. C'est exactement le piège documenté par Bredbenner & Simon (2019) : les GA captent l'attention mais le *texte* transfère la compréhension. SciSense doit prouver que le GA encode l'information *indépendamment* du titre. Δ_spoiler = S9b(Title-only) - S9b(Nude) doit être faible (<0.10) pour un VEC réussi.

La condition **TOC-sim** est le vrai contexte écologique pour les journaux. Le GA est vu en thumbnail minuscule (200px) dans une grille de 6-8 articles. C'est là que P6 (mobile-first) et V7 (lisibilité 50%) sont réellement testés. Si S9b s'effondre à 200px, les micro-ancres (P22) et les labels (V3) sont illisibles — le design a échoué à l'échelle réelle.

La condition **Social-sim** est le contexte écologique pour la dissémination. C'est ce que Ibrahim (2017) mesurait. Le tweet peut dire "Breakthrough: OM-85 dominates evidence" — ce qui spoile Q2 complètement — ou "New review on immunomodulators for pediatric RTIs" — ce qui ne spoile rien. Le contenu du tweet est une variable contrôlable dans le protocole.

**Justification (paper)** : La distinction nude/contextualisé suit la méthodologie de Hollands & Spence (1998, *Applied Cognitive Psychology*) qui montrent que la performance de lecture des graphiques varie significativement selon la présence ou l'absence de contexte textuel. La simulation de plateforme (TOC, social media) suit le paradigme de validité écologique recommandé par Munzner (2014, *Visualization Analysis and Design*) : un résultat en laboratoire (nude) n'est généralisable que s'il tient en condition naturelle (contextualisé). La séparation en 4 conditions permet d'isoler chaque source de variance : design seul (nude), effet du titre (title-only), effet de l'échelle (TOC-sim), effet du texte social (social-sim).

### Priorité d'implémentation

| Phase | Condition | Justification |
|-------|-----------|---------------|
| MVP | Nude uniquement | Isole le design, zéro infrastructure additionnelle |
| V2 | Nude + Title-only | Teste l'effet spoiler — une ligne de texte, trivial à implémenter |
| V3 | + TOC-sim | Requiert un moteur de grille avec distracteurs (croise avec le mode Stream) |
| V4 | + Social-sim | Requiert un générateur de tweets/posts — le plus complexe |

### Ce que les nouvelles variables capturent

**`tab_switched`** — Mesure d'intégrité. Si le participant change d'onglet pendant les 5 secondes d'exposition, le test est **invalidé**. Il ne rentre pas dans les calculs de S9a/S9b/S9c. Détection côté client via `document.visibilitychange`. Pas de punition UX (pas de message d'erreur agressif) — le test est simplement marqué `invalid` en base et le GA suivant est proposé.

**`q1_first_keystroke_ms`** — Proxy de la **latence d'accès mémoire**. Le temps entre l'apparition de Q1 et le premier caractère tapé mesure la vitesse à laquelle le souvenir émerge. Un rappel immédiat (<1500ms) indique un ancrage fort (PH1 T=1s a fonctionné). Un délai long (>5000ms) indique une reconstruction effortée.

**`q1_last_keystroke_ms`** — Combiné avec `q1_first_keystroke_ms`, donne la **durée de production** : `q1_production_ms = q1_last_keystroke_ms - q1_first_keystroke_ms`. Une production longue avec un premier keystroke rapide = le participant a beaucoup à dire (riche encodage). Une production longue avec un premier keystroke lent = il cherche ses mots (encodage faible).

Le profil du participant ajoute 5 covariables :

```
P = {
    clinical_domain,        -- {pediatrician, gp, researcher_bio, tech_data, none}
    data_literacy,          -- {published_author, tech_data, general_public}
    experience_years,       -- {lt5, 5to15, gt15}
    grade_familiar,         -- {0, 1}
    color_vision            -- {normal, colorblind, unknown}
}
```

---

## 2. Les 3 Scores Primaires

### S9a — Reconnaissance Sémantique (Q1)

**Définition** : Le participant a-t-il identifié le sujet du GA ?

**Méthode** : Similarité cosinus entre l'embedding du texte de rappel libre et l'embedding d'une description de référence du GA.

```
S9a(q1_text, ref_text) = {
    1   si cos_sim(embed(q1_text), embed(ref_text)) ≥ θ
    0   sinon
}
```

où :
- `embed()` est un modèle d'embedding de phrases (sentence-transformers, e.g. `all-MiniLM-L6-v2` ou le endpoint Anthropic)
- `ref_text` est la description sémantique attendue, définie dans `ga_metadata`
- `θ` est le seuil de similarité (calibré empiriquement, point de départ : **θ = 0.35**)

Exemple immunomodulateur :
```
ref_text = "Immunomodulators preventing recurrent respiratory tract infections in children, 
            with evidence hierarchy comparing OM-85, PMBL, MV130, and CRL1505"
```

Le scoring par embedding résout le problème fondamental du recall libre : les participants ne répondent pas dans le vocabulaire du concepteur. "Un poumon attaqué par des virus avec des barres de couleurs" et "Graphical abstract sur les immunomodulateurs pédiatriques" désignent le même objet mais partagent zéro mot-clé. La similarité cosinus dans l'espace d'embedding capture cette équivalence sémantique.

**Score continu** : En plus du binaire S9a ∈ {0, 1}, on conserve la valeur continue :

```
S9a_raw(q1_text, ref_text) = cos_sim(embed(q1_text), embed(ref_text))    ∈ [-1, 1]
```

La distribution de `S9a_raw` sur N participants est plus informative que le binaire — elle révèle si les participants sont proches du seuil (signal faible mais présent) ou loin (GA non identifiable).

**Calibration de θ** : Le seuil θ = 0.35 est un point de départ. En phase 2 (N=20-50), on trace la courbe ROC de S9a_raw vs. jugement humain (un annotateur code manuellement "compris / pas compris" sur les 50 rappels) et on choisit θ qui maximise le F1-score. Ce θ calibré devient le standard SciSense pour toutes les missions futures.

**Métrique agrégée** :
```
Taux_S9a(GA) = Σ S9a(i) / N
```
où N = nombre de participants valides ayant testé ce GA.

**Justification du choix (paper)** : Le rappel libre (free recall) est la mesure standard de la rétention en psychologie cognitive depuis Tulving (1962). Nous préférons le rappel libre au rappel indicé (cued recall) car il mesure ce que le participant a spontanément encodé, sans indice qui pourrait reconstruire une mémoire absente. L'utilisation d'embeddings plutôt que de mots-clés pour le scoring automatisé suit la méthodologie de Cer et al. (2018, *SemEval*) qui montre que la similarité cosinus de sentence embeddings corrèle à r=0.78-0.86 avec le jugement humain de similarité sémantique, contre r=0.40-0.55 pour les méthodes lexicales (BLEU, keyword overlap). Le seuil θ est calibré empiriquement par courbe ROC sur un sous-ensemble annoté humainement, suivant la pratique standard en NLP appliqué (Manning et al., 2008).

### Le biais de la modalité de production (Q1) — Voice vs Texte

**Le problème** : Le rappel libre tapé au clavier ne mesure pas la compréhension. Il mesure l'intersection de la compréhension avec la motivation à taper. Un participant qui a parfaitement compris le GA mais écrit "un truc de poumon" par flemme produit un S9a_raw faible — le scoring punit la laziness, pas l'ignorance.

Ce biais a un nom : le **production bottleneck** (Levelt, 1989). La production écrite requiert trois étapes coûteuses que la production orale court-circuite :

1. **Formulation lexicale** — trouver le mot juste ("immunomodulateurs" vs "trucs pour le système immunitaire"). À l'oral, le locuteur utilise des approximations et des périphrases sans friction. À l'écrit, il s'autocensure ("je ne suis pas sûr de l'orthographe, je vais mettre un mot plus simple").
2. **Encodage moteur** — taper sur un clavier est 3-5× plus lent que parler (frappe ~40 mots/minute vs parole ~150 mots/minute, Wobbrock et al., 2006). Le participant optimise inconsciemment le ratio information/effort et coupe du contenu.
3. **Auto-édition** — le texte tapé est visible, relu, corrigé. Le locuteur oral produit un stream of consciousness non filtré, plus proche de la trace mnésique brute.

**La conséquence mesurable** : En condition texte, le rappel Q1 est typiquement 5-15 mots. En condition voice, les études sur le rappel libre verbal montrent des productions de 30-80 mots (Anderson & Conway, 1993, *Memory*). Le scoring sémantique reçoit un input 3-5× plus riche, ce qui augmente mécaniquement la qualité du matching : un vecteur d'embedding calculé sur 50 mots est plus discriminant qu'un vecteur sur 5 mots (la loi des grands nombres s'applique aux dimensions d'embedding).

**Le protocole** : Q1 propose un choix de modalité :

```
"Que venez-vous de voir ?"
    [🎤 Parler]    [⌨️ Taper]
```

Si voice :
1. Enregistrement audio (`MediaRecorder API` → blob webm)
2. Transcription temps réel (SpeechRecognition API browser-native, ou Whisper server-side en V2)
3. Affichage du transcript — le participant voit le texte et peut corriger les erreurs STT
4. Bouton "Valider" — le transcript corrigé devient `q1_text`
5. L'audio est stocké pour traçabilité (`data/audio/{test_id}_q1.webm`)

**Whisper avec vocabulaire guidé (V2)** : L'API Whisper accepte un `initial_prompt` qui biaise la reconnaissance vers un vocabulaire technique. Chaque GA metadata fournit un champ `whisper_prompt` contenant les termes techniques du paper ("immunomodulateurs OM-85 PMBL MV130 CRL1505 épithélium IgA RTI"). La reconnaissance des termes spécialisés passe de ~60% à ~95% avec ce seeding (Radford et al., 2022, *Robust Speech Recognition via Large-Scale Weak Supervision*).

**Variables stockées** :

```
q1_input_mode,          -- 'text' | 'voice'
q1_raw_transcript,      -- STT output AVANT édition utilisateur (null si text)
q1_edit_distance,       -- Levenshtein(raw_transcript, q1_text) — mesure l'erreur STT
q1_audio_path,          -- chemin vers le fichier audio (null si text)
q1_text,                -- texte FINAL (tapé ou transcript validé) — scoré par embedding
```

`q1_text` reste le champ unique d'entrée du scoring sémantique. Que le participant ait tapé ou parlé, `embed(q1_text)` est calculé sur le texte final validé. Le scoring ne change pas. Seul l'input change — il est plus riche en voice.

**Adaptation de la chronométrie keystroke** :

En mode voice, les métriques keystroke (`q1_first_keystroke_ms`, `q1_last_keystroke_ms`) sont remplacées par leurs équivalents vocaux :

| Métrique texte | Équivalent voice | Comment |
|---|---|---|
| `q1_first_keystroke_ms` | `q1_first_utterance_ms` | Temps entre apparition Q1 et début de la première détection vocale (SpeechRecognition `onresult` timestamp) |
| `q1_last_keystroke_ms` | `q1_last_utterance_ms` | Timestamp de la fin du dernier segment vocal détecté |
| `q1_rt` (soumission) | `q1_rt` (clic "Valider") | Identique — mesure le délai de validation post-production |

La latence d'accès (`q1_first_utterance_ms`) est l'**exact analogue** du Voice Onset Time (VOT) en psycholinguistique — le temps entre le stimulus et le début de la production verbale. C'est un proxy encore plus pur de la vitesse de récupération mnésique que le first keystroke, car il ne contient pas la latence motrice du clavier (Levelt, 1989, ch. 12).

**Hypothèse testable (H5)** :

```
H5 : S9a_raw(voice) > S9a_raw(text)
```

Si la voice produit des scores sémantiques systématiquement plus élevés, ça confirme que le bottleneck en condition texte est la production, pas la compréhension. Les deux populations (voice et text) sont marquées par `q1_input_mode` et ne doivent pas être agrégées sans contrôle : la modalité est une covariable dans la régression de phase 4.

```
logit(S9b) = ... + β₇·q1_input_mode
```

Si β₇ est non significatif, la modalité de Q1 n'affecte pas Q2 — les deux modes sont interchangeables pour le scoring. Si β₇ est significatif, la richesse du rappel vocal prédit un meilleur S9b — ce qui suggère que la qualité de l'encodage en mémoire (capturée par Q1) et la lecture de la hiérarchie (Q2) sont couplées.

**Justification du choix (paper)** : La supériorité du rappel oral sur le rappel écrit en termes de volume et de fidélité est documentée depuis Rubin (1977, *Memory & Cognition*) et confirmée par Kvavilashvili & Fisher (2007). Le bottleneck de production écrite a été formalisé par Grabowski (2008, *Written Language & Literacy*) qui montre que la transcription manuelle réduit le contenu du rappel de 30-40% par rapport à la dictée. L'approche bimodale (choix texte/voice) suit le principe d'accessibilité universelle et évite le biais d'exclusion des participants moins à l'aise avec le clavier (personnes âgées, cliniciens sur mobile, locuteurs non-natifs). Le stockage de l'audio brut garantit la traçabilité et permet une ré-analyse future avec des modèles STT améliorés. L'utilisation d'un `initial_prompt` Whisper pour le vocabulaire technique suit la recommandation de Radford et al. (2022) pour les domaines spécialisés.

### S9b — Hiérarchie Perceptive (Q2)

**Définition** : Le participant a-t-il identifié l'élément le mieux documenté ?

```
S9b(q2_choice, correct) = {
    1   si q2_choice == correct
    0   sinon (y compris "Je ne sais pas")
}
```

C'est **la métrique reine**. C'est elle qui valide P32 (longueur), P34 (luminance), V5 (hiérarchie). Si S9b est élevé, le VEC encode correctement. Si S9b est bas, le design est cassé.

**Métrique agrégée** :
```
Taux_S9b(GA) = Σ S9b(i) / N
```

**Seuils de décision** :
- Taux_S9b ≥ 0.80 → **PASS** — le VEC encode correctement
- 0.60 ≤ Taux_S9b < 0.80 → **WARN** — signal présent mais pas dominant
- Taux_S9b < 0.60 → **FAIL** — le design n'encode pas la hiérarchie

**Référence** : GRADE symboles = 74% compréhension (Akl 2007). Le VEC doit battre ce benchmark (≥80%) pour justifier sa supériorité.

**Justification du choix (paper)** : La question à choix forcé (forced-choice) est le standard en psychophysique pour mesurer la discrimination perceptive (Green & Swets, 1966, *Signal Detection Theory*). Le format 4AFC (4-Alternative Forced Choice) + option "Je ne sais pas" évite le biais de devinette : avec 4 options, le taux de chance est 25%. Un taux S9b de 80% représente donc un d' (d-prime) d'environ 2.3, indiquant une forte discrimination. Le seuil de 80% est choisi pour dépasser à la fois le taux de chance (25%) avec p<0.001 (test binomial, N≥10) et le benchmark GRADE (74%, Akl et al., 2007). L'option "Je ne sais pas" est comptée comme incorrect plutôt qu'exclue, suivant la recommandation de Krosnick et al. (2002) qui montrent que l'exclusion des "ne sais pas" surestime la compréhension réelle.

### S9c — Actionnabilité (Q3)

**Définition** : Le participant envisage-t-il un changement de pratique ?

```
S9c(q3_choice) = {
    1.0   si "yes"
    0.5   si "need_more_data"
    0.0   si "no"
}
```

L'échelle 0-0.5-1 capture la nuance : "besoin de plus de données" est une réponse scientifiquement honnête, pas un échec.

**Métrique agrégée** :
```
Score_S9c(GA) = Σ S9c(i) / N     ∈ [0, 1]
```

**Justification du choix (paper)** : L'actionnabilité est la métrique terminale d'un outil de knowledge translation (Grimshaw et al., 2012, *Implementation Science*). Nous utilisons une échelle ordinale à 3 points plutôt qu'un Likert à 5 ou 7 points car : (a) la question est posée après une exposition de 5 secondes — la granularité fine serait du bruit, (b) en condition d'incertitude, les échelles à 3 points produisent des données plus fiables que les échelles fines (Jacoby & Matell, 1971, *Journal of Marketing Research*). La valeur intermédiaire de 0.5 pour "besoin de plus de données" reflète le fait qu'en evidence-based medicine, demander plus de preuves est un comportement rationnel (Djulbegovic & Guyatt, 2017, *The Lancet*), pas un signe d'incompréhension.

---

## 3. Les Métriques Temporelles

### RT₂ — Temps de Décision Hiérarchique

Le temps de réponse à Q2 (`q2_rt`) est un proxy de la **fluence perceptive**. Si le design encode bien, la réponse est rapide. Si le participant hésite, le signal est ambigu.

**Modèle** : RT₂ suit une distribution log-normale (comme tous les temps de réaction cognitifs).

```
log(RT₂) ~ Normal(μ, σ²)
```

On utilise la **médiane** (pas la moyenne) comme statistique de tendance centrale, robuste aux outliers.

```
Médiane_RT₂(GA) = median({q2_rt(i) : i ∈ participants_valides})
```

**Interprétation** :
- Médiane_RT₂ < 3000ms → Décision fluide, le canal perceptif primaire (longueur) a suffi
- 3000ms < Médiane_RT₂ < 8000ms → Hésitation, canaux secondaires mobilisés
- Médiane_RT₂ > 8000ms → Le design ne guide pas la décision

**Justification du choix (paper)** : Les temps de réaction en tâche de décision perceptive suivent une distribution log-normale, pas normale — propriété documentée depuis Luce (1986, *Response Times*) et confirmée par Ratcliff (1993). La médiane est donc l'estimateur approprié de tendance centrale, la moyenne étant biaisée par la queue droite. Le seuil de 3000ms est dérivé de la littérature sur le traitement visuel à deux systèmes (Kahneman, 2011) : le Système 1 (automatique, pré-attentif) traite les features visuelles en <250ms (Treisman & Gelade, 1980) mais la décision complète intégrant mémoire de travail prend 1-3s. Au-delà de 3s, le Système 2 (délibératif, effortful) est engagé — ce qui signifie que le design n'a pas réussi à rendre la hiérarchie "évidente" au sens perceptif.

### Couplage S9b × RT₂

La métrique la plus informative est le **Speed-Accuracy Tradeoff** :

```
                    S9b_correct (répondu juste)
                   /                           \
          RT₂ < 3s                              RT₂ > 3s
        "Fast & Right"                    "Slow & Right"
        (design parfait)                  (signal présent, effort requis)

                    S9b_incorrect (répondu faux)
                   /                           \
          RT₂ < 3s                              RT₂ > 3s
       "Fast & Wrong"                     "Slow & Wrong"
       (design trompe activement)         (design ne guide pas)
```

**"Fast & Wrong"** est le pire cas : le design envoie activement le mauvais signal. C'est exactement le **spin visuel** que Vorland et al. (2024) documentent.

**"Fast & Right"** est l'objectif : le cerveau décode la hiérarchie sans effort conscient, via le traitement pré-attentif (Treisman, <250ms pour les features ; la décision complète prend 1-3s).

### Invalidation : Tab Switch

```
valid(T) = {
    0   si tab_switched == true
    1   sinon
}
```

Un test invalidé est **enregistré mais exclu** de tous les calculs de S9a/S9b/S9c et des métriques temporelles. On ne le supprime pas — le taux d'invalidation lui-même est informatif :

```
Taux_invalidation(GA) = Σ (1 - valid(i)) / N_total
```

Un taux d'invalidation élevé (>20%) signale un problème UX (le brief n'a pas préparé le participant) ou un GA trop peu engageant (le participant s'ennuie et switch).

L'implémentation côté client est simple : `document.addEventListener('visibilitychange', ...)`. Dès que `document.hidden == true` pendant la phase d'exposition, `tab_switched = true`. Pas de message d'erreur agressif — juste un flag silencieux.

**Tous les N dans ce document sont des N_valides** : `N = Σ valid(i)`.

**Justification du choix (paper)** : L'exclusion des essais avec interruption d'attention est standard en psychophysique (Pashler, 1998, *The Psychology of Attention*). Un changement d'onglet pendant l'exposition réduit la durée de stimulation effective à une valeur inconnue, invalidant la comparabilité avec les essais complets (5000ms). Nous choisissons l'exclusion silencieuse plutôt que l'exclusion punitive (message d'erreur) pour deux raisons : (a) éviter l'effet de demande (demand characteristics — Orne, 1962) où le participant modifie son comportement parce qu'il se sent surveillé, (b) le taux d'invalidation lui-même est une métrique diagnostique de la qualité UX et de l'engagement. Les essais invalides sont *conservés en base* avec le flag `tab_switched=1` pour analyse secondaire — ils pourraient révéler des patterns (par ex. les profils "grand public" switchent plus que les cliniciens).

### Chronométrie Keystroke — La Dynamique du Rappel (Q1)

Le rappel libre (Q1) est la seule question ouverte. Les timestamps keystroke donnent 3 métriques dérivées qui racontent comment le souvenir émerge :

```
Latence d'accès     = q1_first_keystroke_ms
Durée de production = q1_last_keystroke_ms - q1_first_keystroke_ms
Délai de validation = q1_rt - q1_last_keystroke_ms
```

**Latence d'accès** (`q1_first_keystroke_ms`) :

Le temps avant la première frappe est un proxy de la vitesse de récupération mnésique. Le GA a disparu — le participant fouille sa mémoire de travail.

| Latence | Interprétation |
|---------|---------------|
| < 1500ms | Ancrage immédiat. Le choc cognitif PH1 (T=1s) a imprimé une trace forte. |
| 1500-4000ms | Récupération standard. L'information est là mais demande un effort. |
| > 4000ms | Reconstruction. Le participant ne se souvient pas clairement et compose. |

**Durée de production** (`q1_last_keystroke_ms - q1_first_keystroke_ms`) :

La longueur de la frappe, combinée à la latence, crée une matrice 2×2 :

```
                    Production courte          Production longue
                    (< 3000ms)                 (> 3000ms)
                 ┌────────────────────┬────────────────────┐
  Latence        │                    │                    │
  courte         │  Flash : sait      │  Riche : sait      │
  (< 1500ms)     │  exactement quoi   │  et a beaucoup     │
                 │  dire, le dit vite │  à dire             │
                 ├────────────────────┼────────────────────┤
  Latence        │                    │                    │
  longue         │  Minimal : cherche │  Laborieux : ne se │
  (> 1500ms)     │  puis résume en    │  souvient pas      │
                 │  un mot            │  clairement        │
                 └────────────────────┴────────────────────┘
```

"Flash" et "Riche" sont les bons signaux — le GA a imprimé. "Laborieux" corrèle avec S9a faible.

**Délai de validation** (`q1_rt - q1_last_keystroke_ms`) :

Le temps entre la dernière frappe et la soumission. Si > 3000ms, le participant relit et hésite. Si < 500ms, il soumet sans relire. Informatif pour la confiance subjective mais pas intégré au scoring.

**Justification du choix (paper)** : La décomposition du temps de réponse en latence d'initiation + durée de production + délai de validation est un paradigme standard en psycholinguistique (Levelt, 1989, *Speaking: From Intention to Articulation*). La latence d'initiation (time to first keystroke) est l'analogue écrit du voice onset time (VOT) utilisé en production verbale — elle mesure le temps de planification pré-articulatoire, qui est un proxy direct de l'accessibilité de la représentation en mémoire de travail (Baddeley, 2003). La durée de production reflète la quantité d'information encodée (Cowan, 2001, *The magical number 4*). La décomposition keystroke a été validée pour le scoring automatisé de rappel par Kalyuga & Sweller (2005) dans le contexte de la charge cognitive, et par Grabowski (2008) pour la mesure de la fluence rédactionnelle. Nous utilisons `performance.now()` (résolution sub-milliseconde, W3C High Resolution Time Level 2) plutôt que `Date.now()` (résolution ~15ms) pour garantir la précision temporelle.

---

## 4. Stratification par Profil

### La Matrice 2D

Les 2 axes du profil créent 4 quadrants :

```
                        Littératie Analytique
                    Basse               Haute
                 ┌───────────────┬───────────────┐
    Expertise    │               │               │
    Clinique     │  Q1: Public   │  Q2: Tech     │
    Basse        │  naïf         │  (Nicolas)    │
                 │               │               │
                 ├───────────────┼───────────────┤
                 │               │               │
    Expertise    │  Q3: Clinicien│  Q4: Clinicien│
    Clinique     │  non-data     │  + chercheur  │
    Haute        │               │               │
                 │               │               │
                 └───────────────┴───────────────┘
```

**Hypothèses testables** :

| Hypothèse | Prédiction | Ce que ça prouve si vrai |
|-----------|-----------|------------------------|
| H1 : Le VEC est universel | Taux_S9b(Q1) ≈ Taux_S9b(Q2) ≈ Taux_S9b(Q3) ≈ Taux_S9b(Q4) | Le design porte le savoir indépendamment de l'expertise |
| H2 : La littératie data aide | Taux_S9b(Q2) > Taux_S9b(Q1) | Les profils analytiques décodent mieux les barres (attendu) |
| H3 : L'expertise clinique court-circuite | Taux_S9b(Q4) > Taux_S9b(Q2) | La connaissance du domaine ajoute un canal (reconnaissance vs décodage) |
| H4 : Le daltonisme casse le signal | Taux_S9b(colorblind) < Taux_S9b(normal) | V14 n'est pas résolu |
| H5 : La voice capture mieux | S9a_raw(voice) > S9a_raw(text) | Le bottleneck est la production écrite, pas la compréhension |

**Test statistique** : Chi² d'indépendance (S9b binaire × quadrant catégoriel). Requiert N≥5 par cellule = N≥20 minimum. Fisher exact si N<5 par cellule.

**Justification du choix (paper)** : La matrice 2D (Expertise Clinique × Littératie Analytique) est motivée par la dissociation documentée entre domain knowledge et graph literacy dans la compréhension des représentations visuelles. Garcia-Retamero & Cokely (2017, N=27 885, 60 pays) ont montré que la numératie (notre axe Littératie) prédit la compréhension des aides visuelles indépendamment de l'expertise médicale. Okan et al. (2012, *Health Expectations*) confirment que la graph literacy — pas l'éducation générale — est le prédicteur dominant de l'interprétation correcte des graphiques de risque. H1 (universalité) est l'hypothèse la plus forte : si le VEC fonctionne, les quadrants ne devraient PAS différer significativement sur S9b, car le design compense les différences d'expertise. Un résultat non-significatif au chi² (p>0.05) est ici le résultat *souhaité* — ce qui justifie un calcul de puissance pour le risque β (erreur de type II) plutôt que le seul risque α. Avec N=20 par cellule (N=80 total) et α=0.05, la puissance de détecter un effet modéré (w=0.3) au chi² est de 85%.

---

## 5. Le Delta de Correction Cognitive (A/B Testing — V2)

Quand l'A/B séquentiel sera implémenté, chaque participant verra d'abord un GA contrôle (industrie) puis un GA VEC. Le delta mesure l'élimination du spin.

### Définition

```
Δ_S9b(participant_i) = S9b(VEC) - S9b(contrôle)     ∈ {-1, 0, +1}
```

Au niveau agrégé :

```
Δ̄_S9b = Taux_S9b(VEC) - Taux_S9b(contrôle)
```

### Interprétation

| Δ̄_S9b | Signification |
|--------|--------------|
| > +0.30 | Le VEC élimine massivement le spin. Publiable. |
| +0.10 à +0.30 | Amélioration modérée. Le design aide mais ne domine pas. |
| -0.10 à +0.10 | Pas de différence. Le VEC n'est pas meilleur que l'industrie. |
| < -0.10 | Le VEC est PIRE. Alarme design. |

### Test statistique

Les données sont appariées (même participant, deux conditions). Test de McNemar sur la table 2×2 :

```
                    VEC correct     VEC incorrect
Contrôle correct        a                b
Contrôle incorrect      c                d
```

```
χ² = (b - c)² / (b + c)
```

Si χ² > 3.84 (seuil p=0.05, 1 ddl) → différence significative.

**Puissance** : Pour détecter un Δ̄_S9b = 0.30 avec 80% de puissance et α=0.05, McNemar requiert N ≈ 30 paires. Avec un effet de 0.40 (attendu si le contrôle utilise l'aire comme encodage primaire et le VEC utilise la longueur), N ≈ 20 paires suffisent.

**Justification du choix (paper)** : Le test de McNemar (1947) est le test exact pour comparer deux proportions appariées sur données binaires. Le design intra-sujet (within-subject) est choisi plutôt qu'inter-sujet (between-subject) car il contrôle automatiquement toutes les variables individuelles (expertise, numératie, motivation) — chaque participant est son propre contrôle. Cela réduit la variance d'erreur et donc le N requis d'un facteur ~2-4 par rapport à un design entre-groupes (Fleiss et al., 2003, *Statistical Methods for Rates and Proportions*). L'ordre séquentiel (contrôle d'abord, VEC ensuite) introduit un biais d'apprentissage potentiel — le participant pourrait mieux performer sur l'image VEC simplement parce qu'il a compris le format. Ce biais joue *contre* notre hypothèse si le contrôle est aussi un GA, et *pour* notre hypothèse si le contrôle est un format très différent. En phase 4 (N=500+), un contrebalancement (randomisation de l'ordre) éliminera ce biais. Pour la phase 3 (N=30), le biais est documenté et accepté comme limitation. Le calcul de puissance suit Lachin (1992, *Controlled Clinical Trials*) pour le test de McNemar.

---

## 6. Temporalité de la Preuve

### Phase 1 : Test Manuel (N=3-5, cette semaine)

Pas de statistique inférentielle possible. Données descriptives :
- Taux_S9b brut (ex: 4/5 = 80%)
- Rappels libres Q1 (analyse qualitative)
- RT₂ si mesurable (chronomètre téléphone)

**Critère de décision** : ≥4/5 correct sur S9b → go soumission MDPI

### Phase 2 : MVP Localhost (N=20-50)

Premiers tests d'hypothèse :
- Chi² S9b × profil (si N≥20)
- Médiane RT₂ avec intervalle interquartile
- Taux S9a, S9b, S9c par GA
- **Taux d'invalidation (tab switch)** — si >20%, diagnostic UX
- **Distribution latence d'accès Q1** — histogramme par profil
- **Corrélation latence Q1 × S9a** — la latence prédit-elle la reconnaissance ?

### Phase 3 : A/B Testing (N=30+)

McNemar sur paires contrôle/VEC :
- Δ̄_S9b avec intervalle de confiance
- Stratification par quadrant si N≥80 (20 par cellule)

### Phase 4 : Données de masse (N=500+)

Régression logistique :
```
logit(S9b) = β₀ + β₁·clinical_domain + β₂·data_literacy + β₃·grade_familiar 
           + β₄·color_vision + β₅·ga_version + β₆·log(q1_first_keystroke_ms)
           + β₇·q1_input_mode
```

β₅ est le coefficient du VEC : son effet net sur la compréhension, contrôlé pour toutes les covariables du profil.

β₆ teste si la latence d'accès mémoire (Q1) prédit indépendamment le succès sur Q2. Si β₆ est significatif et négatif (accès rapide → meilleure hiérarchie), cela confirme que l'ancrage PH1 et le décodage P32 sont couplés : un bon choc cognitif en Zone 1 prédit une bonne lecture de la Zone 3.

β₇ teste si la modalité de production (voice vs texte) affecte S9b. Si non significatif → les deux modes sont interchangeables. Si significatif et positif → la richesse du rappel vocal prédit un meilleur décodage hiérarchique — ce qui suggère que Q1 et Q2 mesurent des facettes couplées du même encodage mnésique.

**Justification du choix (paper)** : La régression logistique est le modèle standard pour les variables dépendantes binaires en recherche clinique (Hosmer & Lemeshow, 2013, *Applied Logistic Regression*). La log-transformation de la latence Q1 (`log(q1_first_keystroke_ms)`) est nécessaire car les temps de réaction sont log-normalement distribués (Luce, 1986) — inclure la valeur brute violerait l'hypothèse de linéarité du logit. L'inclusion simultanée des covariables de profil et de la version du GA dans un modèle unique permet de tester l'effet du VEC *contrôlé pour* les différences individuelles — c'est l'équivalent statistique de la question "le design fait-il la différence, à profil constant ?". Si β₅ est significatif après contrôle, l'effet est attribuable au design, pas à la composition de l'échantillon. L'ajout de β₆ teste une hypothèse mécaniste (le couplage ancrage-décodage) qui, si confirmée, fournit une explication causale de l'efficacité du VEC, pas seulement une corrélation.

---

## 7. Le Score Composite (pour le dashboard)

Pour le `GET /api/stats` et l'affichage post-test, un score unique par test :

```
Score_S2b = (0.2 × S9a) + (0.5 × S9b) + (0.3 × S9c)     ∈ [0, 1]
```

Pondération :
- S9b pèse 50% car c'est la métrique reine (le VEC encode-t-il la hiérarchie ?)
- S9c pèse 30% car l'actionnabilité est le but final
- S9a pèse 20% car le rappel libre a la variance la plus élevée (dépend du vocabulaire, de la fluence rédactionnelle)

**Affichage** :
- Score_S2b ≥ 0.70 → "Décodage réussi"
- Score_S2b < 0.70 → "Le design n'a pas survécu au transfert"

**Justification du choix (paper)** : Le score composite est une commodité opérationnelle, pas une variable primaire d'analyse. Dans le paper, les 3 scores (S9a, S9b, S9c) seront rapportés séparément comme recommandé par les guidelines CONSORT pour les outcomes multiples (Moher et al., 2010). Le composite sert au dashboard temps réel et à la gamification (V2). Les poids (0.2/0.5/0.3) reflètent la hiérarchie de validité : S9b est un 4AFC avec taux de chance connu (25%) et scoring objectif ; S9c est un ordinal à 3 niveaux avec scoring semi-arbitraire (0/0.5/1) ; S9a dépend du modèle d'embedding et du seuil θ. Dans un paper formel, ces poids seraient dérivés empiriquement par analyse factorielle ou par Analytic Hierarchy Process (Saaty, 1980). Pour le MVP, ils sont fixés a priori et documentés comme tels.

---

## 8. Justification du Protocole d'Exposition — Du Spotlight au Stream

### Le biais du Spotlight

Le protocole initial (brief → countdown → image isolée 5s) place le participant en condition d'**attention focalisée** (spotlight attention). Le brief active le Système 2 (Kahneman, 2011). Le countdown pré-alloue la mémoire de travail. Le participant *sait* qu'il va devoir se souvenir de quelque chose et *sait* exactement quand ça va arriver.

C'est l'inverse du contexte écologique. Le pédiatre qui scrolle sa TOC MDPI à 23h est en **attention ambiante** : son regard balaie des thumbnails, des titres, des GAs — il ne sait pas lequel va l'interpeller. L'attention n'est pas *dirigée* vers le GA, elle est *capturée* par lui (ou pas). La différence est fondamentale en psychophysique : la capture attentionnelle (exogenous attention) est bottom-up et dépend des propriétés du stimulus, tandis que l'attention dirigée (endogenous attention) est top-down et dépend de l'instruction (Posner, 1980; Theeuwes, 2010).

Un protocole spotlight surestime systématiquement les taux S9a/S9b car il élimine la compétition attentionnelle. Le VEC ne sera jamais vu en condition spotlight dans la vraie vie.

### Le protocole Stream (v2)

Le GA cible est inséré dans un **flux d'éléments visuels** simulant un scroll de TOC.

```
FLUX = [distracteur₁, distracteur₂, ..., GA_cible, ..., distracteur_n]
```

**Structure du flux :**

| Paramètre | Valeur | Justification |
|-----------|--------|---------------|
| Nombre d'éléments | 5-8 par séquence | Simule une page de TOC MDPI (~6-10 articles) |
| Position du GA cible | Aléatoire (position 2 à N-1) | Le participant ne peut pas prédire quand préparer son attention |
| Durée par élément | 3-5s (variable) | La variance empêche le comptage. Durée moyenne calibrée sur les données d'eye-tracking de scroll mobile (Liu et al., 2020) |
| Distracteurs | Vrais GAs/thumbnails d'autres articles | Écologiquement valides — pas des carrés gris |
| Question testée | Élément aléatoire parmi les 3 derniers vus | Le participant doit encoder *tous* les éléments, pas juste le GA cible |

**Le flux UX :**

```
[Écran briefing simplifié]
    "Vous allez voir défiler une série d'images scientifiques.
     Après le défilement, nous vous poserons des questions 
     sur l'une d'entre elles."
    ☑ J'ai compris

[Flux : éléments défilent, 3-5s chacun, transition fluide]
    distracteur₁ (thumbnail d'un article, 4s)
    distracteur₂ (GA réel d'un autre paper, 3s)
    GA_CIBLE (le GA VEC à tester, 4s)
    distracteur₃ (figure d'article, 5s)
    distracteur₄ (GA industrie, 3s)

[Écran de sélection]
    "Sur quelle image portent les questions ?"
    → Affichage de 3 thumbnails miniatures (le GA cible + 2 distracteurs)
    → Le participant clique sur celui qu'il pense reconnaître
    → Ça peut être n'importe lequel des 3

[Questions S2b sur l'image sélectionnée]
    Q1, Q2, Q3 comme avant
```

### Ce que le Stream ajoute au modèle

**Nouvelle métrique : Saillance (S10)**

```
S10(GA) = P(participant sélectionne le GA cible comme "l'image dont il se souvient")
```

Si le participant voit 5 images et qu'on lui en montre 3 dont le GA cible, S10 mesure la probabilité que le GA soit l'image *spontanément retenue*. Le taux de chance est 1/3 = 0.33.

| S10 | Interprétation |
|-----|---------------|
| > 0.70 | Le GA capture l'attention dans un flux — scroll-stopping validé |
| 0.33-0.70 | Le GA n'est pas plus mémorable que les distracteurs |
| < 0.33 | Le GA est activement ignoré (pire que le hasard) |

S10 mesure ce que les altmetrics prétendent mesurer (engagement, scroll-stopping) mais avec un protocole contrôlé. C'est le pont entre l'attention (que la littérature documente) et la compréhension (que nous mesurons).

**Couplage S10 × S9b : La Chaîne Complète**

```
Saillance (S10) → Reconnaissance (S9a) → Hiérarchie (S9b) → Action (S9c)
     "je l'ai vu"       "je sais ce que         "je sais qui      "je ferais
                          c'est"                  est le mieux"     autrement"
```

Pour qu'un GA produise un impact clinique, TOUTE la chaîne doit tenir. Un GA avec S10=0.90 et S9b=0.30 est un piège : il arrête le scroll mais trompe le lecteur (spin). Un GA avec S10=0.40 et S9b=0.95 est invisible : il encode parfaitement mais personne ne le regarde.

Le VEC doit maximiser le produit : `S10 × S9b`.

**Justification du choix (paper)** : Le paradigme de flux avec distracteurs est l'adaptation au contexte digital du paradigme RSVP (Rapid Serial Visual Presentation) utilisé en psychologie de l'attention depuis Potter (1975, *Cognitive Psychology*). Potter a montré que les images présentées brièvement (~250ms) dans un flux peuvent être identifiées mais pas mémorisées, tandis qu'à 2-5 secondes la mémorisation est robuste — ce qui correspond à notre fenêtre d'exposition. L'insertion d'un stimulus cible parmi des distracteurs écologiquement valides suit le paradigme du "attentional blink" (Raymond, Shapiro & Arnell, 1992) adapté aux durées longues. La sélection post-flux (reconnaissance parmi 3 thumbnails) est un test de reconnaissance standard (Mandler, 1980), plus écologique que le rappel forcé car il simule le moment où le lecteur décide de "revenir" à un élément aperçu dans son scroll. La mesure combinée S10 × S9b est analogue au framework Signal Detection Theory (Green & Swets, 1966) appliqué en deux étapes : d'abord détecter le signal (S10 = hit rate de la saillance), puis le décoder (S9b = accuracy de l'interprétation).

### Deux modes, une plateforme

Le protocole S2b supporte les deux modes sur la même plateforme :

| Mode | Quand | Ce qu'il mesure | Validité |
|------|-------|----------------|----------|
| **Spotlight** | Quick test, crash test Nicolas, validation rapide | Compréhension en attention maximale (ceiling) | Interne — borne supérieure |
| **Stream** | Protocole complet, données pour le paper | Compréhension en attention ambiante (écologique) | Externe — généralisable |

Le mode est taggé dans `test_results` (`exposure_mode = 'spotlight' | 'stream'`). Les deux modes produisent des données comparables (mêmes S9a/S9b/S9c) mais ne doivent jamais être agrégés ensemble — ils mesurent des conditions cognitives différentes.

**Implémentation** : Le mode spotlight reste pour le MVP localhost (rapide à coder, rapide à tester). Le mode stream est la V2 — il requiert une bibliothèque de distracteurs et un moteur de randomisation de position. Mais la DB et le scoring sont identiques.

### Mise à jour de la durée d'exposition

La justification des 5000ms tient pour les deux modes :

**Contrainte écologique** : Les études d'eye-tracking sur le scroll mobile montrent un temps de fixation moyen de 2-5 secondes par élément (Liu et al., 2020). En mode stream, la durée par élément varie entre 3-5s pour empêcher le comptage et simuler le rythme naturel du scroll.

**Contrainte cognitive** : Le modèle PH1 prédit 3 phases (T=1s flux chromatique, T=2s ancrage/fracture, T=3s décision). 5 secondes donnent 2 secondes de marge, permettant au Système 1 de compléter son traitement.

**Contrainte statistique** : En mode spotlight, la durée fixe élimine la variance inter-sujets. En mode stream, la variance contrôlée (3-5s) est documentée et analysable comme covariable.

---

## 9. Résumé des Métriques

### Métriques de Scoring

| Métrique | Formule | Ce qu'elle mesure | Seuil |
|----------|---------|------------------|-------|
| **S10** | **P(sélection du GA cible)** | **Le GA capture-t-il l'attention dans un flux ?** | **>0.70** |
| Taux_S9a | Σ S9a / N | Le GA est-il identifiable ? | ≥0.60 |
| **Taux_S9b** | **Σ S9b / N** | **La hiérarchie est-elle perçue ?** | **≥0.80** |
| Score_S9c | Σ S9c / N | Le GA déclenche-t-il l'action ? | ≥0.40 |
| **S10 × S9b** | **Saillance × Hiérarchie** | **La chaîne complète tient-elle ?** | **>0.56** |
| Score_S2b | 0.2·S9a + 0.5·S9b + 0.3·S9c | Score composite | ≥0.70 |
| Δ̄_S9b | S9b(VEC) - S9b(ctrl) | Le VEC bat-il l'industrie ? | >+0.30 |
| **Δ_spoiler** | **S9b(title_only) - S9b(nude)** | **Le titre porte-t-il l'info à la place du GA ?** | **<+0.10** |

### Métriques Temporelles

| Métrique | Formule | Ce qu'elle mesure | Seuil | Mode |
|----------|---------|------------------|-------|------|
| Médiane_RT₂ | median(q2_rt) | Fluence de la décision hiérarchique | <3000ms | tous |
| Latence_Q1 | q1_first_keystroke_ms / q1_first_utterance_ms | Vitesse d'accès mémoire | <1500ms = ancrage fort | text / voice |
| Production_Q1 | q1_last - q1_first | Richesse du souvenir encodé | informatif | text / voice |
| Validation_Q1 | q1_rt - q1_last | Confiance subjective | informatif | text / voice |
| **Word_count_Q1** | **len(q1_text.split())** | **Volume du rappel** | **voice > text attendu** | **tous** |

### Métriques d'Intégrité, Saillance et Modalité

| Métrique | Formule | Ce qu'elle mesure | Seuil |
|----------|---------|------------------|-------|
| Taux_invalidation | Σ tab_switched / N_total | Fiabilité du flux de test | <0.20 |
| **S10 (stream only)** | **P(sélection GA cible)** | **Capture attentionnelle en flux** | **>0.70** |
| S10 × S9b | Saillance × Hiérarchie | Chaîne complète attention→compréhension | >0.56 |
| **Δ_modalité** | **S9a_raw(voice) - S9a_raw(text)** | **La voice capture-t-elle mieux le rappel ?** | **>0 attendu (H5)** |

---

## 10. Schéma DB mis à jour

Colonnes additionnelles pour `test_results` :

```sql
-- Condition d'exposition
ALTER TABLE test_results ADD COLUMN exposure_mode TEXT DEFAULT 'spotlight';        -- 'spotlight' | 'stream'
ALTER TABLE test_results ADD COLUMN exposure_condition TEXT DEFAULT 'nude';         -- 'nude' | 'title_only' | 'toc_sim' | 'social_sim'
ALTER TABLE test_results ADD COLUMN stimulus_frame TEXT;                            -- 'none' | 'mdpi_grid' | 'twitter_card' | 'linkedin_card'
ALTER TABLE test_results ADD COLUMN stimulus_text TEXT;                             -- texte accompagnant (null si nude)
ALTER TABLE test_results ADD COLUMN stimulus_image_width INTEGER;                   -- px effectifs (200, 500, 550)

-- Intégrité
ALTER TABLE test_results ADD COLUMN tab_switched INTEGER DEFAULT 0;                -- 0|1
ALTER TABLE test_results ADD COLUMN exposure_actual_ms INTEGER;                     -- ≤5000

-- Keystroke dynamics (Q1) — mode text
ALTER TABLE test_results ADD COLUMN q1_first_keystroke_ms INTEGER;                  -- ms
ALTER TABLE test_results ADD COLUMN q1_last_keystroke_ms INTEGER;                   -- ms

-- Voice input (Q1) — mode voice
ALTER TABLE test_results ADD COLUMN q1_input_mode TEXT DEFAULT 'text';              -- 'text' | 'voice'
ALTER TABLE test_results ADD COLUMN q1_raw_transcript TEXT;                         -- STT avant édition user (null si text)
ALTER TABLE test_results ADD COLUMN q1_edit_distance INTEGER;                       -- Levenshtein(raw, validated) — mesure erreur STT
ALTER TABLE test_results ADD COLUMN q1_audio_path TEXT;                             -- chemin audio blob (null si text)
ALTER TABLE test_results ADD COLUMN q1_first_utterance_ms INTEGER;                  -- voice: onset de la première détection vocale
ALTER TABLE test_results ADD COLUMN q1_last_utterance_ms INTEGER;                   -- voice: fin du dernier segment vocal
ALTER TABLE test_results ADD COLUMN q1_word_count INTEGER;                          -- nombre de mots dans q1_text final

-- Stream mode
ALTER TABLE test_results ADD COLUMN stream_position INTEGER;                        -- position GA cible dans le flux
ALTER TABLE test_results ADD COLUMN stream_length INTEGER;                          -- nombre d'éléments total
ALTER TABLE test_results ADD COLUMN stream_selected_id TEXT;                        -- GA choisi par le participant
ALTER TABLE test_results ADD COLUMN s10_hit INTEGER;                                -- 1 si sélection correcte

-- Embedding (S9a sémantique)
ALTER TABLE test_results ADD COLUMN s9a_raw REAL;                                   -- cos_sim brute ∈ [-1, 1]
```

Côté JS (`arena.js`), les events à capturer :

```javascript
// Intégrité
document.addEventListener('visibilitychange', () => {
    if (document.hidden && state === 'EXPOSURE') {
        data.tab_switched = true;
        data.exposure_actual_ms = performance.now() - exposureStart;
    }
});

// Keystroke timing Q1
const q1Input = document.getElementById('q1-text');
q1Input.addEventListener('keydown', (e) => {
    const now = performance.now() - q1Start;
    if (!data.q1_first_keystroke_ms) data.q1_first_keystroke_ms = now;
    data.q1_last_keystroke_ms = now;
});

// Tous les timestamps via performance.now() (sub-ms, W3C HR Time Level 2)
// Pas Date.now() (~15ms résolution)
```

---

*La beauté n'a aucune corrélation avec la compréhension.*
*Seuls les chiffres savent si l'information a survécu au transfert.*