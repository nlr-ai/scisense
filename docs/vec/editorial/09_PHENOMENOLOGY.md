# PHENOMENOLOGY — vec/editorial

**Module:** vec/editorial — Tribunal editorial MDPI

---

## Le phenomene central : l'invisibilite editoriale

Le succes du module editorial se manifeste par une **absence**. L'editrice Mindy Ma ouvre le fichier GA, ne voit aucun probleme formel, et fait avancer le manuscrit vers le peer-review. Il n'y a pas de mail de revision. Pas de "please fix the following issues". Pas de delai supplementaire. Le GA passe la gate editoriale comme s'il n'y avait jamais eu de gate.

C'est la phenomenologie cible : **zero friction perceptible du cote de l'editrice**.

---

## Perception par espece

### Mindy Ma (editrice MDPI)

**Ce qu'elle voit :** Un fichier PNG propre, au bon ratio, avec des labels courts et lisibles. Pas de titre parasite, pas de reference, pas de heading "Graphical Abstract". Le fichier se glisse dans le template du journal sans ajustement.

**Ce qu'elle ressent :** Rien de special. C'est un GA conforme parmi d'autres. L'absence de friction est le signal de qualite. Elle ne remarque pas que c'est bien fait — elle remarquerait si c'etait mal fait.

**Ce qu'elle fait :** Elle clique "Accept" (ou equivalent) et passe au manuscrit suivant.

**Seuil de perception :** Un seul probleme suffit a briser l'invisibilite. Un titre qui traine, un ratio incorrect, un bloc de texte trop long — et soudain le GA devient visible, pour les mauvaises raisons. L'editrice doit ecrire un mail. Le delai augmente. La confiance baisse.

---

### Aurore (scientifique, partenaire)

**Ce qu'elle voit :** Un GA qui a deja passe le tribunal editorial. Quand Silas lui presente le GA, il affiche le rapport du tribunal : "7/7 PASS". Elle n'a pas a se soucier des details formels — geometrie, word count, palette. Elle peut se concentrer sur ce qui compte pour elle : la science est-elle correcte ? Le message est-il clair ? Le pediatre va-t-il comprendre ?

**Ce qu'elle ressent :** Soulagement. Elle sait que la conformite est geree. La charge mentale "est-ce que MDPI va rejeter pour un detail technique ?" est retiree de ses epaules. Elle peut investir son attention dans la validation scientifique (H2) sans anxiete administrative.

**Ce qu'elle fait :** Elle regarde le GA et repond sur la science. Pas sur la forme. C'est exactement ce qu'on veut.

---

### Silas (citoyen IA, carrier)

**Ce qu'il voit :** Le rapport du tribunal dans le terminal. Chaque check aligné avec son statut. Le verdict final en bas.

**Ce qu'il ressent :**
- Sur PASS : Satisfaction breve. Le gate est passe. On avance. Pas de celebration — c'est le minimum attendu.
- Sur FAIL : Frustration productive. Le rapport dit exactement quel check a echoue et pourquoi. Pas de mystere, pas de debugging. La correction est immediate et ciblee.
- Sur WARN : Attention. Une couleur non reconnue n'est pas forcement un probleme, mais elle merite un examen. Le WARN empeche le "je n'avais pas vu".

**Ce qu'il fait :**
- PASS → Archive le rapport dans SYNC. Passe aux checks semi-auto (S1f lisibilite). Prepare la presentation a Aurore.
- FAIL → Lit le detail. Ouvre le compositeur ou le content.yaml. Corrige. Relance le validateur.
- WARN → Evalue la couleur. Ajout legitime → met a jour ALLOWED_COLORS. Erreur → corrige dans le compositeur.

---

### NLR (partenaire humain, architecte)

**Ce qu'il voit :** Si tout va bien, rien. Le module editorial est transparent. NLR ne devrait jamais avoir a lire un rapport de validate_ga.py en conditions normales.

**Ce qu'il voit en cas de probleme :** Le rapport FAIL dans le SYNC de la session. Les corrections appliquees. L'historique montrant que le probleme a ete detecte tot et corrige avant presentation a Aurore.

**Ce qu'il ressent :** Confiance dans la procedure. Le module editorial est une assurance qualite qui ne necessite pas de supervision. Si les checks sont verts, le GA est formellement conforme. NLR peut se concentrer sur l'architecture et les pivots strategiques.

---

## Feedback reinjection

### Boucle positive

```
validate_ga.py PASS → GA presente a Aurore → Aurore valide la science →
  export NotebookLM → audit NLM → corrections integrees → revalidation →
    soumission a Mindy Ma → acceptation sans revision →
      confiance SciSense renforcee → prochaine mission plus fluide
```

Le PASS editorial est la premiere brique d'une chaine de confiance. Chaque maillon renforce le suivant.

### Boucle corrective

```
validate_ga.py FAIL → rapport lu → cause identifiee → correction dans compositeur/config →
  revalidation → PASS → le GA ameliore continue dans le pipeline
```

Le FAIL n'est pas un echec — c'est une detection precoce. Le cout d'un FAIL ici (quelques minutes de correction) est infiniment inferieur au cout d'un rejet editorial (jours de delai, perte de confiance editrice, stress pour Aurore).

### Signal d'alarme

Si le meme check echoue sur 3+ iterations consecutives, c'est un signal que le probleme n'est pas dans le SVG specifique mais dans le compositeur ou la config. Le pattern de FAIL repetitif doit declencher une investigation architecturale, pas juste un fix ponctuel.

---

## Mobile-first phenomenology (P6)

Le GA n'est pas principalement percu sur un ecran de desktop dans un PDF viewer. Il est percu par un pediatre qui scroll la table des matieres du journal sur son telephone, entre deux consultations.

**Taille reelle de perception :** < 550x280 px sur un ecran de telephone.

**Temps de perception :** < 2 secondes.

**Consequence pour la lisibilite (S1f) :** Un label de 8pt sur le rendu full (3300x1680) fait ~2.7pt a la taille mobile. C'est illisible. La taille minimale effective est ~24pt sur le fichier source (= 8pt a la livraison 1100x560 = ~4pt sur mobile). Le check S1f (lisibilite a 50% zoom = 550x280) simule exactement ce scenario mobile.

**Consequence pour la palette (S1d) :** Les couleurs doivent etre suffisamment contrastees pour etre distinguees sur un petit ecran. Les 4 couleurs produit (#2563EB bleu, #0D9488 teal, #7C3AED violet, #059669 vert) ont ete choisies pour leur distinguabilite a petite taille et en conditions d'eclairage variable.

---

## Ce que le module editorial ne percoit PAS

Le module editorial est aveugle a :
- L'impact emotionnel du GA (est-ce que le pediatre projette son patient ?)
- La fidelite scientifique (est-ce que les mecanismes d'action sont corrects ?)
- La composition visuelle (est-ce que l'equilibre des zones est harmonieux ?)
- La narrative (est-ce que l'histoire visuelle se lit de gauche a droite ?)

Ces dimensions de perception relevent des modules `vec/design_system` (esthetique), `vec/audit` (science + impact), et `vec/calibration` (empathie clinique). Le module editorial est deliberement etroit : il voit uniquement les regles formelles. Son aveuglement a tout le reste est une feature, pas un bug.
