# PATTERNS — vec/editorial

**Module:** vec/editorial — Tribunal editorial MDPI

---

## P1: Gate binaire — pas de score partiel

La conformite editoriale MDPI est un predicat booleen. 7/7 ou FAIL. Il n'existe pas de "presque conforme". Un GA avec un ratio incorrect est rejete exactement comme un GA avec 6 violations. Le verdict du script est un exit code : 0 ou 1.

**Implication code :** `validate()` retourne `(bool, str)`. Le bool est le seul signal qui compte pour la gate. Le string est le rapport pour le debugging.

---

## P2: Separation producteur / validateur

Le compositeur (`compose_ga_v10.py`) ne valide jamais sa propre sortie. Le validateur (`validate_ga.py`) ne produit jamais de GA. Ce sont deux scripts, deux responsabilites, deux moments du pipeline. Le compositeur produit avec optimisme. Le validateur juge avec intransigeance.

**Corollaire :** Si un check echoue, la correction se fait dans le compositeur ou dans la config, jamais dans le validateur. Le validateur ne "fixe" rien — il detecte.

---

## P3: Fail Loud — pas de silence

Tout echec est rapporte avec la raison exacte. Le rapport du tribunal affiche chaque check avec PASS/WARN/FAIL et le detail. Un check silencieusement ignore est pire qu'un check absent — il cree une fausse confiance.

**Implication code :** Chaque fonction `check_*` retourne un `(status, detail)`. Le detail n'est jamais vide. Meme en cas de PASS, le detail confirme ce qui a ete verifie (ex: "27/30 words", "all 4 product colors present").

---

## P4: Source de verite YAML pour les donnees parametriques

Les constantes qui varient entre missions (palette, budget texte, labels attendus) vivent dans des fichiers YAML (`palette.yaml`, `content.yaml`). Le script les charge. Les constantes MDPI universelles (ratio, forbidden patterns, regles textuelles) sont hardcodees dans le script — elles ne changent pas entre missions.

**Regle :** Si une constante change quand on change de mission, elle va dans YAML. Si elle change quand MDPI change ses regles, elle va dans le script.

---

## P5: Checks auto vs. semi-auto — frontiere explicite

| Type | Checks | Carrier | Quand |
|------|--------|---------|-------|
| **Auto** | S1a (geometry), S1b (word count), S1c (no titles), S1d (palette), S1e (no GA heading), S1g (forbidden patterns) | Silas (script) | Avant chaque presentation |
| **Semi-auto** | S1d mission (non-redondance Fig1/Fig2), S1f (lisibilite 50% zoom) | Silas (verification visuelle) + Aurore | Apres le PASS auto, avant soumission |
| **Manuel** | S1e mission (droits visuels / provenance) | Silas (checklist PROVENANCE.md) | Avant soumission finale |

La frontiere n'est pas un echec d'automatisation — c'est une reconnaissance que certains jugements sont irreductiblement humains. Automatiser la lisibilite a 50% zoom avec un seuil arbitraire creerait plus de faux positifs qu'il n'en eliminerait.

---

## P6: Mobile-first (herite de GA_SPEC.md section 2.6bis)

Le GA est vu principalement sur telephone mobile, dans la table des matieres du journal. La taille d'affichage reelle est souvent inferieure a 1100x560 px. Toute decision editoriale (taille de police minimale, densite de labels, choix des couleurs) doit etre evaluee dans le contexte du rendu mobile, pas du rendu desktop plein ecran.

**Implication pour S1f :** Le test de lisibilite a 50% zoom (550x280 px) n'est pas un test extreme — c'est le cas d'usage reel du pediatre qui scroll la table des matieres sur son telephone entre deux consultations.

---

## P7: Idempotence

Executer `validate_ga.py` deux fois sur le meme SVG produit exactement le meme rapport. Le script ne modifie rien, ne cache rien, n'a pas d'etat. C'est une fonction pure : SVG in, rapport out.

---

## P8: Pas de faux sentiment de completude

Le script valide 7 checks. La conformite MDPI reelle en comporte davantage (format de fichier, DPI, espace couleur sRGB, absence de filigrane). Les checks non implementes sont documentes explicitement dans le HEALTH (08_HEALTH.md) comme loops ouvertes. Ne jamais dire "7/7 PASS = MDPI conforme" — dire "7/7 PASS = editorial gate passee, checks restants semi-auto/manuels".
