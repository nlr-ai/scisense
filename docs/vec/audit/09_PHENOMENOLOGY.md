# Phenomenology — vec/audit

## PH-AUD1: Comment Aurore percoit le processus d'audit

Aurore ne voit pas l'audit. Elle voit un GA qui arrive avec un message clair : "voila ce qu'on a fait, voila les 2-3 points ou on a besoin de toi". Le travail de NotebookLM, l'export, les corrections — tout ca est invisible pour elle. Ce qu'elle percoit :

- **Confiance :** Le GA qu'on lui presente a deja ete passe au crible. Les bugs techniques sont corriges. Les incoherences ont ete traitees. Elle ne decouvre pas de problemes embarrassants.
- **Respect de son temps :** Pas de page blanche. Pas de question vague. Des options concretes, chacune avec ses consequences. Elle choisit en 5 minutes, pas en 2 heures.
- **Fierte :** Quand elle valide, elle sait que c'est solide. Les findings NLM qu'on partage ("NotebookLM a confirme que la hierarchie des preuves est correcte") renforcent sa confiance dans le livrable.
- **Simplicite :** Un PNG, 2-3 points en gras, repondre oui ou choisir A/B/C. Le processus derriere est complexe — sa surface est simple.

**Si l'audit rate :** Aurore decouvre des erreurs techniques, des metaphores incorherentes, des violations MDPI. Sa confiance dans le processus chute. Le perfectionnisme se reveille : "je dois tout verifier moi-meme". Le gain de temps est perdu. La paralysie revient.

## PH-AUD2: Comment NotebookLM percoit le GA

NotebookLM opere sur un contexte plat : les fichiers de S0N/. Il ne voit pas l'historique des versions (sauf si on le pollue). Il ne voit pas le code Python. Ce qu'il voit :

- La science (doc chain mission : mecanismes, preuves, produits)
- Les contraintes (MDPI, invariants, patterns du Design System)
- Le rendu courant (PNG delivery + SVG)
- Le system prompt qui definit son role (auditeur, pas directeur)

Son output est une photographie instantanee de la coherence entre la science et le visuel. Chaque session est une coupe — pas un flux continu. C'est pour ca que le Hard Reset fonctionne : chaque session est independante si l'export est propre.

**Ce que NotebookLM fait bien :** Detecter les incoherences entre fichiers, mapper les patterns violes, synthetiser des suggestions multi-sources, produire des formats varies (report/slides/podcast/infographie).

**Ce que NotebookLM ne fait PAS bien :** Juger l'impact clinique sur un pediatre (c'est le domaine d'Aurore). Ecrire du code SVG (c'est le domaine de Silas). Maintenir un contexte propre sur plusieurs sessions (d'ou P11/PA5).

## PH-AUD3: Comment Silas percoit l'audit

L'audit est le moment ou Silas soumet son travail a deux jugements exterieurs. Ce n'est pas un examen — c'est un miroir.

- **NotebookLM** est un miroir systematique : il voit des patterns que Silas, plonge dans le code, ne voit plus. Le bouclier qui flotte, la couleur qui se repete, la densite qui etouffe. Des choses visibles de l'exterieur, invisibles de l'interieur.
- **Aurore** est un miroir clinique : elle voit si la science est fidele, si le message passe, si le pediatre comprend. Des choses que ni le code ni l'analyse textuelle ne peuvent verifier.

La tension productive : chaque finding est un moment ou Silas doit decider — corriger, rejeter avec justification, ou escalader. Pas de rejet silencieux (VN-AUD3). Pas de soumission aveugle non plus. L'audit developpe le jugement de Silas autant qu'il ameliore le GA.

## PH-AUD4: Comment le feedback se propage

```
NotebookLM identifie "le bouclier OM-85 flotte"
    → Silas traduit : "P18 viole — embodiment actif manque"
    → Silas corrige : bouclier encastre SUR les briques
    → Re-rendu : nouveau PNG delivery
    → Presentation Aurore : "On a encastre le bouclier sur les briques
       pour montrer que OM-85 agit a la surface. Tu valides?"
    → Aurore : "Oui, c'est mieux — mais est-ce que le texte 'OM-85'
       est assez visible?"
    → Silas traduit : P28 hierarchie typo Niveau 2 — verifier font-size
    → Correction + re-rendu
    → Nouveau cycle H6 si necessaire
```

Le finding voyage : NLM (analyse) → Silas (traduction + correction) → Aurore (validation). Chaque etape enrichit. Aucune ne fait le travail des autres.

## PH-AUD5: Le podcast comme outil de decantation

Le podcast NotebookLM est un format sous-estime. Quand deux voix synthetiques "racontent" le GA, elles mettent des mots sur des choix visuels que l'analyse textuelle laisse implicites. Ecouter le podcast revele :

- Les transitions narratives maladroites (le flux L→R se casse quelque part)
- Les metaphores qui ne passent pas a l'oral (si la voix ne sait pas decrire le bouclier, le pediatre non plus)
- Le rythme : un podcast qui stagne sur la Zone 2 = la densite est trop haute
- L'absence : ce que le podcast ne mentionne pas est ce que le GA ne communique pas

Le podcast n'est pas un livrable. C'est un instrument de perception — il permet d'entendre ce que le GA dit, pas seulement de le voir. Transcription via `transcribe_podcast.py` pour archivage et reference.
