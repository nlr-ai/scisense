# Behaviors — vec/design_system

3 behaviors observables du design system. Chaque behavior est un effet visible dans le GA final.

---

## DS-B4: Le cercle vicieux est brise (extends B4 mission)

**Ce qui se passe:** La transition visuelle gauche→droite (rouge→vert, poreux→intact) montre que l'intervention brise la boucle pathologique. Le cercle vicieux ferme en Zone 1 (4 stations : Viral RTIs → Th2 bias → Remodeling → Re-susceptibility) est physiquement fracture par une lance verte (health arrow) qui traverse le trace rouge.

**Ce que le pediatre percoit:** Une forme circulaire rouge fermee (= piege, boucle sans issue) qui est brisee par un vecteur vert (= intervention, resolution). Le message est immediat : "quelque chose brise le cycle de la maladie".

**Contraintes design system:**
- Le cercle vicieux DOIT etre une fleche circulaire fermee, pas un schema lineaire. La forme geometrique EST le message (P23).
- La lance verte DOIT traverser physiquement le cercle, pas le contourner ou le fondre. C'est un acte graphique explicite (SD3 slide 15).
- Des marques de fracture (eclats, lignes de rupture) doivent etre visibles au point d'impact.
- Le rouge #DC2626 du cycle est le meme rouge que les virus — cohesion chromatique pathologique.
- La lance utilise le vert composite des 4 produits ou le vert de sante general (#059669-derived).

**Implements:** P23 (resolution topologique), B4 (breaking the cycle).
**Verified by:** H8 (S8a lance brise cycle, S8b marques de fracture).
**Delivers:** DS-R4 (fracture du cercle vicieux).

---

## DS-B5: Les 4 couleurs-produits sont constantes (extends B5 mission)

**Ce qui se passe:** Les couleurs OM-85=#2563EB (bleu), PMBL=#0D9488 (teal), MV130=#7C3AED (violet), CRL1505=#059669 (vert) sont utilisees partout : icones metaphoriques, barres d'evidence, fleches de flux, lignes de convergence, et legende. Le pediatre associe couleur = produit sans legende.

**Ce que le pediatre percoit:** Quatre teintes distinctes reviennent de maniere coherente a travers le GA. En Zone 2, il voit 4 agents colores sur le tissu. En Zone 3, il voit 4 barres de la meme couleur avec des remplissages proportionnels. Le lien est automatique : le bleu ici = le bleu la-bas = meme produit.

**Contraintes design system:**
- Aucune substitution de couleur. Les hex codes sont fixes dans palette.yaml.
- Aucun degrade inter-produit qui brouille l'identite (un degrade bleu→teal rendrait OM-85 et PMBL indistinguables).
- Le rouge #DC2626 est reserve exclusivement aux elements pathologiques. JAMAIS utilise pour un produit.
- Les teintes de fond (bandes anatomiques, background) ne doivent pas entrer en conflit avec les couleurs produit. Utiliser des neutres desatures.

**Implements:** P7 (coherence chromatique).
**Verified by:** H1 palette sub-check (grep hex codes dans SVG) + DS-H1.
**Delivers:** DS-R1 (coherence chromatique).

---

## DS-B8: Convergence visuelle IgA (extends B8 mission)

**Ce qui se passe:** Les 4 flux-produits (OM-85 bleu, PMBL teal, MV130 violet, CRL1505 vert) convergent visuellement vers un point focal unique dans le lumen : le site de synthese des IgA muqueuses. Les 4 couleurs se rejoignent physiquement dans l'espace du GA, formant un noeud visuel.

**Ce que le pediatre percoit:** 4 traces de couleurs differentes venant de 4 directions/mecanismes distincts qui arrivent au meme point. Des petits Y (IgA) au point de rencontre. Le message est "4 agents, 1 resultat" — l'objectif tissulaire est unique quel que soit le mecanisme d'action en amont.

**Contraintes design system:**
- Les 4 flux doivent etre visuellement distincts (pas de superposition qui brouille les couleurs). Chaque flux garde sa couleur produit.
- Le point focal est dans le **lumen apical** — pas dans le mur, pas dans la lamina propria. Les IgA sont secretees dans la lumiere bronchique.
- Les formes Y (IgA) sont des micro-ancres moleculaires (P22), ~15px, regroupees au point de convergence.
- L'arc CRL1505 arrive d'en bas (systemique, P19) mais converge vers le meme point que les 3 agents locaux.
- Le point de convergence est le climax scientifique — il doit avoir un poids visuel adequat sans dominer les enfants (P31).

**Implements:** P3 (compression metaphorique), P19 (topologie spatiale), B8 (convergence IgA).
**Verified by:** H7 (S7a 4 lignes colorees, S7b formes Y au point focal).
**Delivers:** DS-R3 (convergence visuelle IgA).

---

## Relations inter-behaviors

```
DS-B5 (couleurs constantes) → prerequis de DS-B8 (convergence IgA)
   Les 4 flux de convergence ne sont lisibles que si les couleurs sont constantes et distinctes.

DS-B4 (cycle fracture) → contrepartie narrative de DS-B8 (convergence)
   DS-B8 est le climax scientifique ("4 agents, 1 resultat").
   DS-B4 est le climax narratif ("le cycle est brise").
   Ensemble ils forment la tension et la resolution du GA.

DS-B5 (couleurs) → renforce DS-B4 (fracture)
   Le rouge du cycle est le meme rouge que les virus (coherence pathologique).
   Le vert de la lance est derive du vert CRL1505 (coherence therapeutique).
```
