# Objectives — vec/audit

## O-AUD1: Goal

Garantir que le GA qui sort de la compilation est scientifiquement fidele, visuellement coherent et editorialement propre AVANT qu'il ne soit presente a Aurore pour validation finale. L'audit est le filet de securite entre le code de Silas et le jugement d'Aurore.

Deux intelligences complementaires (P13) ferment cette garantie :
- **NotebookLM** audite en profondeur (multi-sources, patterns, coherence globale)
- **Aurore** tranche la science et l'impact clinique (V5, PH1)

Delivers R-AUD1 (science validee), R-AUD2 (audit NLM integre).

## Non-Goals

- **NO-AUD1: Pas de directives de code.** NotebookLM liste des problemes, des patterns applicables et des suggestions. Il ne dit JAMAIS a Silas "configure tel YAML" ou "ajuste telle coordonnee". Silas est autonome sur l'implementation (P13, system prompt V2.4 section 4).

- **NO-AUD2: Pas de validation MDPI automatisee.** Les checks S1a-S1g sont la responsabilite de `vec/editorial`. L'audit peut signaler une violation MDPI, mais le checker automatise vit dans l'autre module.

- **NO-AUD3: Pas de substitution au jugement d'Aurore.** NotebookLM ne decide pas si la hierarchie des preuves est correcte. Il peut signaler une incoherence, mais la decision revient a Aurore. Aurore decide la science, NotebookLM audite, Silas code.

- **NO-AUD4: Pas de session NotebookLM perpetuelle.** Chaque session a un objectif clair, un export propre, et un output exploitable. Si le contexte se pollue (P11), on fait un Hard Reset — pas une session de plus.

## Priorites (ranked)

1. Fidelite scientifique — les mecanismes biologiques encodes dans le GA sont corrects (V5, P3)
2. Coherence visuelle — les patterns du Design System sont respectes (P18-P23, P26-P31)
3. Integrite editoriale — les invariants MDPI ne sont pas violes (V1-V7)
4. Completude de la boucle — chaque probleme identifie a une resolution tracable

## Tradeoffs

- **T-AUD1: Profondeur d'audit vs vitesse de livraison.** Un audit exhaustif retarde la soumission. Mais un GA avec une erreur scientifique detruit la credibilite d'Aurore. On favorise la profondeur. T4 (mission-level) fixe la borne : VN3 (jamais de brouillon) reste inviolable.

- **T-AUD2: Nombre de cycles NLM vs rendements decroissants.** Le premier cycle d'audit produit 80% des findings. Le deuxieme en capture 15%. Au-dela, le risque de sur-optimisation depasse le gain. 2-3 cycles par version majeure.

- **T-AUD3: Autonomie de Silas vs findings NLM.** Quand NotebookLM suggere une correction et Silas juge qu'elle degrade un autre aspect, Silas documente le conflit dans SYNC et escalade a Aurore ou NLR. Il ne rejette pas silencieusement.
