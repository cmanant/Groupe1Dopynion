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
À chaque fin de tour :
1. **Ranger** les cartes jouées dans la défausse
2. **Piocher** pour revenir à 5 cartes en main
3. Si le deck est vide → mélanger la défausse qui devient le nouveau deck

---

*Projet dans le cadre du cours Sciences de l'Ingénieur - Gestion de projet et développement d'API HTTP*