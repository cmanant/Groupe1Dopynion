# Groupe1Dopynion

## Règles du Jeu - Gestion de Royaume

### Objectif
Gérer un royaume et obtenir le plus de points de victoire possible en construisant un deck de cartes optimal. Le classement évolue selon un système ELO : plus vous battez un adversaire fort, plus vous montez dans le classement.

### Configuration de départ
- **10 cartes par joueur** au démarrage :
  - **7 cartes Copper** (Cuivre - trésor)
  - **3 cartes Estate** (Domaine - points de victoire)
- **5 cartes en main** au début de chaque tour
- **10 types de cartes action** disponibles (choisis par l'arbitre)

### Composition des cartes
- **Cartes Trésor** : permettent d'acheter d'autres cartes
- **Cartes Victoire** : donnent des points en fin de partie (incluent Estate, Province, etc.)
- **Cartes Action** : déclenchent des effets spéciaux

### La Réserve (le "magasin")
**Cartes Trésor** (quantités fixes) :
- **60 Copper** (Cuivre)
- **40 Silver** (Argent) 
- **30 Gold** (Or)

**Cartes Victoire** (selon le nombre de joueurs) :
- **2 joueurs** : 8 cartes de chaque type
- **3-4 joueurs** : 12 cartes de chaque type
- **Max 4 joueurs** par partie

**Cartes Action** :
- **10 cartes** de chaque type choisi par l'arbitre

### Déroulement d'un tour
Le jeu se déroule en **3 phases** :

#### 1. Phase Action
- Jouer **1 carte action** maximum par tour (par défaut)
- La carte doit être **dans votre main** pour être jouée
- Au démarrage, aucune carte action disponible (seulement Copper et Estate)
- Les cartes action peuvent déclencher des effets sur les royaumes adverses

#### 2. Phase Achat
- Utiliser les cartes trésor pour acheter de nouvelles cartes
- Acheter des cartes trésor, victoire ou action depuis la réserve

#### 3. Phase Ajustement
- Ranger les cartes utilisées
- Piocher de nouvelles cartes pour compléter sa main

### Gestion des piles de cartes
- **Deck** : votre pioche (mélangée au démarrage)
- **Main** : 5 cartes visibles par vous seul
- **Défausse** : cartes jouées temporairement, reviendront en jeu
- **Rebut** : poubelle définitive, cartes éliminées de la partie
- **Réserve** : le "magasin" commun pour acheter des cartes

#### Cycle des cartes
- Quand le deck est vide lors d'une pioche → la défausse est mélangée et devient le nouveau deck
- Les cartes jouées vont en défausse et reviendront périodiquement
- Les cartes au rebut sont définitivement perdues

### Conditions de fin de partie
La partie s'arrête **immédiatement** quand une de ces conditions est déclenchée (le tour en cours se termine, mais pas le tour de table) :

1. **Toutes les cartes Province** sont achetées (12 ou 8 selon le nombre de joueurs)
2. **3 piles de la réserve** sont complètement vides
3. **150 tours maximum** atteints (protection contre l'inactivité)
4. **Action illégale** → élimination du joueur fautif (la partie continue sans lui)

**Actions illégales** : réponse invalide, achat non autorisé, format de réponse incorrect

### Décompte des points
Les points de victoire sont comptés en additionnant **toutes les cartes de victoire possédées** :
- Dans le **deck**
- Dans la **main** 
- Dans la **défausse**

⚠️ **Les cartes au rebut ne comptent pas** (elles ne vous appartiennent plus)

### Phase d'ajustement
À Cr :
1. **Ranger** les cartes jouées dans la défausse
2. **Piocher** pour revenir à 5 cartes en main
3. Si le deck est vide → mélanger la défausse qui devient le nouveau deck

### Accès compte rendu
Lien compte rendu : https://nosy-verdict-e0d.notion.site/2852160e7f5b80d5b21dfd14d2f722ef?v=2852160e7f5b808b9639000c96e77146&p=2852160e7f5b801ba6c1c47c6e6e6c04&pm=s

#### Liste des cartes 
Trésors : 
Copper – 0 – Trésor
+1 pièce.

Silver – 3 – Trésor
+2 pièces.

Gold – 6 – Trésor
+3 pièces.

Cursed Gold – 4 – Trésor (custom)
Quand tu le joues : +3 pièces et tu gagnes 1 Curse (si disponible).

Victoire

Estate – 2 – Victoire
+1 point de victoire.

Duchy – 5 – Victoire
+3 points de victoire.

Province – 8 – Victoire
+6 points de victoire.

Colony – 11 – Victoire
+10 points de victoire.

Gardens – 4 – Victoire (custom Dominion)
Score en fin de partie : +1 point de victoire par tranche de 10 cartes dans ton deck (deck complet : pioche + main + défausse + cartes en jeu).

Malédiction
Curse – 0 – Malédiction
−1 point de victoire.

Actions / Attaques “classiques”
Village – 3 – Action
+1 carte, +2 actions.

Smithy – 4 – Action
+3 cartes.
Market – 5 – Action
+1 carte, +1 action, +1 achat, +1 pièce.

Festival – 5 – Action
+2 actions, +1 achat, +2 pièces.

Laboratory – 5 – Action
+2 cartes, +1 action.

Woodcutter – 3 – Action
+1 achat, +2 pièces.

Council Room – 5 – Action
+4 cartes, +1 achat.
Chaque autre joueur pioche 1 carte.

Distant Shore – 6 – Action
+2 cartes, +1 action.
Quand tu la joues : tu gagnes 1 Estate.

Farming Village – 4 – Action
Révèle des cartes de ton deck jusqu’à trouver une Action ou un Trésor : la carte trouvée va en main, le reste va en défausse.
Ensuite : +2 actions.

Hireling – 6 – Action – Durée “permanente”
Effet continu tant qu’elle reste en jeu : au début de chacun de tes tours, +1 carte supplémentaire (dans ton moteur local on la garde en in_play pour matérialiser l’effet).

Chancellor – 3 – Action
+2 pièces.
Optionnel (dans la version complète) : tu peux défausser tout ton deck dans ta défausse.

Attaques
Witch – 5 – Action – Attaque
+2 cartes.
Chaque autre joueur gagne 1 Curse (si des Curses restent dans la pile).

Militia – 4 – Action – Attaque
+2 pièces.
Chaque autre joueur doit défausser jusqu’à n’avoir plus que 3 cartes en main.

Bandit – 5 – Action – Attaque
Tu gagnes 1 Gold.
Chaque autre joueur révèle les 2 premières cartes de son deck, trash 1 Trésor non-Copper (Gold en priorité sinon Silver), puis défausse les cartes restantes.

Bureaucrat – 4 – Action – Attaque
Tu gagnes 1 Silver sur le dessus de ton deck.
Chaque autre joueur met une carte Victoire de sa main sur le dessus de son deck (s’il en a).

Actions custom / support

Artificer – 5 – Action (custom)
+1 carte, +1 action, +1 pièce.
Ensuite tu peux défausser autant de cartes de ta main que tu veux :
– X = nombre de cartes réellement défaussées,
– tu gagnes une carte de coût X (suivant la logique de ta strat).

Marquis – 6 – Action (custom)
+1 achat.
Tu pioches jusqu’à avoir une main de taille 10 (dans l’implémentation actuelle : draw équivalent à la taille initiale de ta main, puis tu défausses jusqu’à revenir à 10 cartes si tu dépasses).

Poacher – 4 – Action (custom)
+1 carte, +1 action, +1 pièce.
Puis tu défausses 1 carte de ta main par pile vide dans la réserve.

Harvest – 5 – Action (custom)
Révèle les 4 premières cartes de ton deck.
Compte le nombre de types différents parmi ces cartes (Trésor / Action / Victoire / Malédiction, etc.).
Tu pioches jusqu’à 1 carte par type distinct (max 4), puis tu défausses toutes les cartes révélées.

Mag Pie – 4 – Action (custom)
+1 carte, +1 action.
Révèle la prochaine carte de ton deck :
– si c’est un Trésor : tu la pioches, et tu gagnes 1 Mag Pie supplémentaire (si la pile Mag Pie n’est pas vide),
– sinon : tu remets la carte sur le dessus du deck.

Port – 4 – Action (custom)
+1 carte, +1 action.
Effet “on buy” : quand tu achètes un Port, tu gagnes 1 Port supplémentaire (si la pile permet).

Remake – 4 – Action (custom)
Tu choisis une carte de ta main à trash.
Tu gagnes une carte coûtant exactement 1 de plus (selon la logique choisie par ta stratégie).

*Projet dans le cadre du cours Sciences de l'Ingénieur - Gestion de projet et développement d'API HTTP*
