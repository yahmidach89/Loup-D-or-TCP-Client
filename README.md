
# Loup d'Or - Client

## Description

**Loup d'Or - Client** est une application cliente qui permet à un joueur de se connecter à un serveur de jeu multijoueur. Le jeu met en avant des rôles, des interactions et des déplacements dans un univers ludique. Ce client est écrit en Python et utilise une connexion TCP pour communiquer avec le serveur.

## Fonctionnalités

- Connexion au serveur via TCP.
- Définition d'un nom de joueur et d'un rôle parmi : `villageois`, `vif d'or`, `loup garou`.
- Navigation dans un univers en utilisant des commandes de déplacement (`nord`, `sud`, `est`, `ouest`).
- Interaction avec des objets dans l'environnement.
- Consultation de l'état actuel du jeu : carte, objets à proximité, temps restant.
- Gestion des erreurs et des validations côté client.
- Déconnexion sécurisée du serveur.

## Prérequis

- Python 3.6 ou supérieur.
- Le serveur de jeu doit être opérationnel et accessible via l'adresse IP et le port spécifiés.

## Installation

1. Clonez ce dépôt ou téléchargez les fichiers :
   ```bash
   git clone <url_du_dépôt>
   cd <nom_du_dossier>
   ```

2. Assurez-vous que le serveur est configuré et opérationnel.

3. Exécutez le script client.

## Utilisation

1. **Lancez le client** :
   ```bash
   python client.py
   ```

2. **Saisissez votre nom de joueur** lorsque demandé.

3. **Choisissez un rôle** parmi les options disponibles (`villageois`, `vif d'or`, `loup garou`).

4. **Utilisez les commandes** suivantes pour interagir avec le jeu :
   - `set_role` : Définir ou modifier votre rôle (avant que la partie commence).
   - `move <direction>` : Déplacer votre personnage dans une direction (nord, sud, est, ouest).
   - `interact <objet>` : Interagir avec un objet.
   - `get_game_state` : Consulter l'état actuel du jeu.
   - `quit` : Quitter le jeu.

5. **Déconnectez-vous** proprement en utilisant la commande `quit` ou avec `Ctrl+C`.

## Exemple

```bash
$ python client.py
Connecté au serveur.
Bienvenue dans le Loup d'Or !

Entrez votre nom : Yanis
Bienvenue Yanis !

Voici les rôles disponibles : villageois, vif d'or, loup garou
Veuillez en choisir un : loup garou
Rôle attribué : loup garou

Commandes disponibles : set_role, move, interact, get_game_state, quit
Entrez une commande : move nord
Déplacement effectué : {'x': 1, 'y': 2}

Entrez une commande : interact coffre
Résultat de l'interaction : Vous avez trouvé une clé !

Entrez une commande : quit
Déconnecté du serveur.
```

## Structure du Code

- **`GameClient`** : Classe principale implémentant la logique du client.
  - `connect()` : Établit la connexion avec le serveur.
  - `send_request()` : Gère l'envoi et la réception des requêtes au serveur.
  - `set_name()` : Définit le nom du joueur.
  - `set_role()` : Définit le rôle du joueur avant le début du jeu.
  - `move()` : Permet au joueur de se déplacer dans une direction donnée.
  - `interact()` : Permet au joueur d'interagir avec des objets dans le jeu.
  - `get_game_state()` : Récupère l'état actuel du jeu depuis le serveur.
  - `disconnect()` : Ferme proprement la connexion avec le serveur.

## Commandes Disponibles

- `set_role` : Définit ou change le rôle du joueur avant le début de la partie.
- `move <direction>` : Déplace le joueur dans une direction donnée.
  - Directions valides : `nord`, `sud`, `est`, `ouest` (ou leurs équivalents anglais).
- `interact <objet>` : Interagit avec un objet dans l'environnement du joueur.
- `get_game_state` : Affiche l'état actuel du jeu.
- `quit` : Quitte le jeu et déconnecte le joueur.

## Notes Importantes

- Les déplacements et interactions ne sont possibles qu'une fois la partie commencée.
- Le serveur doit être actif et en attente des connexions pour que le client fonctionne correctement.

## Auteurs

- **Nom de l'auteur** : [AHMIDACH Yanis]
- **Contact** : [yahmidach@gmail.com]

## Licence

Ce projet est sous licence [MIT](https://opensource.org/licenses/MIT). Vous êtes libre de le modifier et de le distribuer.
