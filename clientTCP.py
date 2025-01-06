import socket
import json

class GameClient:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.role = None
        self.player_name = None
        self.game_started = False
        self.socket = None

    def connect(self):
        """Établit une connexion TCP avec le serveur."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.server_address, self.server_port))
            print("Connecté au serveur.")
        except Exception as e:
            print("Erreur de connexion au serveur :", e)
            exit()

    def send_request(self, action):
        """Envoie une requête au serveur et retourne la réponse."""
        try:
            # Créer un message JSON avec l'action et le payload
            message = json.dumps({"action": action})
            self.socket.sendall(message.encode())

            # Recevoir la réponse du serveur
            response = self.socket.recv(4096).decode()
            return json.loads(response)
        except Exception as e:
            print("Erreur lors de l'envoi de la requête :", e)
            return None
        
    # def subscribe(self):
    #     """Envoie une requête au serveur et retourne la réponse."""
    #     try:
    #         # Créer un message JSON avec l'action et le payload
    #         message = json.dumps({"role": self.role, "pseudo": self.player_name})
    #         self.socket.sendall(message.encode())

    #         # Recevoir la réponse du serveur
    #         response = self.socket.recv(4096).decode()
    #         print(response)
    #         return json.loads(response)
    #     except Exception as e:
    #         print("Erreur lors de l'envoi de la requête :", e)
    #         return None

    def subscribe(self):
        """Envoie une requête au serveur et retourne la réponse."""
        try:
            # Créer un message JSON avec l'action et le payload
            message = json.dumps({"role": self.role, "pseudo": self.player_name})
            print(message)
            self.socket.sendall(message.encode())

            # Recevoir la réponse du serveur
            response = self.socket.recv(4096).decode()

            if response:
                response_json = json.loads(response)
                return response_json
            else:
                print("Erreur : Aucune réponse reçue du serveur.")
                return None
        except Exception as e:
            print("Erreur lors de l'envoi de la requête :", e)
            return None


    def set_name(self, name):
        """Définit le nom du joueur."""
        self.player_name = name

    # def set_role(self, role):
    #     if self.game_started:
    #         print("Erreur : Vous ne pouvez plus changer de rôle après le début de la partie.")
    #         return

    #     roles = ['villageois', 'vif d\'or', 'loup garou']
    #     if role not in roles:
    #         print("Erreur : Rôle invalide. Choisissez parmi :", roles)
    #         return

    #     response = self.subscribe()
    #     if response and response.get("status") == "success":
    #         self.role = role
    #         print(f"Rôle attribué : {role}")
    #     else:
    #         print("Erreur lors de la définition du rôle :", response.get("message", "Réponse invalide."))

    def set_role(self, role):
        if self.game_started:
            print("Erreur : Vous ne pouvez plus changer de rôle après le début de la partie.")
            return

        roles = ['villageois', 'vif d\'or', 'loup garou']
        if role not in roles:
            print("Erreur : Rôle invalide. Choisissez parmi :", roles)
            return

        response = self.subscribe()
        if response:
            if response.get("status") == "success":
                self.role = role
                print(f"Rôle attribué : {role}")
            else:
                print("Erreur lors de la définition du rôle :", response.get("message", "Réponse invalide."))
        else:
            print("Erreur lors de la définition du rôle : aucune réponse du serveur.")

    def move(self, direction):
        if not self.game_started:
            print("Erreur : Vous ne pouvez pas vous déplacer avant que la partie commence.")
            return

        valid_directions = {
            'NORTH': 'NORTH', 'NORD': 'NORTH', 'N': 'NORTH',
            'SOUTH': 'SOUTH', 'SUD': 'SOUTH', 'S': 'SOUTH',
            'EAST': 'EAST', 'EST': 'EAST', 'E': 'EAST',
            'WEST': 'WEST', 'OUEST': 'WEST', 'O': 'WEST', 'W': 'WEST'
        }

        direction_upper = direction.upper()
        normalized_direction = valid_directions.get(direction_upper)
        if not normalized_direction:
            print("Erreur : Direction invalide. Choisissez parmi :", list(valid_directions.keys()))
            return

        response = self.send_request("move", {"direction": normalized_direction, "player_name": self.player_name})
        if response and response.get("status") == "success":
            print("Déplacement effectué :", response.get("new_position"))
        else:
            print("Erreur lors du déplacement :", response.get("message", "Réponse invalide."))

    def interact(self, object_name):
        if not self.game_started:
            print("Erreur : Vous ne pouvez pas interagir avant que la partie commence.")
            return

        response = self.send_request("interact", {"object_name": object_name, "player_name": self.player_name})
        if response and response.get("status") == "success":
            print("Résultat de l'interaction :", response.get("result"))
        else:
            print("Erreur lors de l'interaction :", response.get("message", "Réponse invalide."))

    def get_game_state(self):
        response = self.send_request("get_game_state", {"player_name": self.player_name})
        if response and response.get("status") == "success":
            data = response.get("data", {})
            self.game_started = data.get("game_started", False)
            print("Carte actuelle :", data.get("map"))
            print("Objets autour :", data.get("nearby_objects"))
            print("Temps restant :", data.get("time_remaining"))
            print("Partie commencée :", self.game_started)
        else:
            print("Erreur lors de la récupération de l'état :", response.get("message", "Réponse invalide."))

    def execute_command(self, command, *args):
        print(command)
        commands = {
            "set_role": lambda: self.set_role(*args),
            "move": lambda: self.move(*args) if args else print("Erreur : Veuillez préciser une direction (nord, sud, est, ouest)."),
            "interact": lambda: self.interact(*args),
            "get_game_state": lambda: self.get_game_state(),
        }

        if command in commands:
            commands[command]()
        else:
            print(f"Erreur : Commande '{command}' non reconnue.")

    def disconnect(self):
        """Ferme la connexion avec le serveur."""

        self.socket.close()
        print("Déconnecté du serveur.")

if __name__ == "__main__":
    server_address = "172.25.1.10"
    server_port = 9999

    client = GameClient(server_address, server_port)
    client.connect()

    print("Bienvenue dans le Loup d'Or !\n")
    while not client.player_name:
        player_name = input("Entrez votre nom : ").strip()
        if player_name:
            client.set_name(player_name)
            client.subscribe()
        else:
            print("Erreur : Le nom ne peut pas être vide. Veuillez réessayer.")

    while client.role is None:
        print("Voici les rôles disponibles : villageois, vif d'or, loup garou")
        client.set_role(input("Veuillez en choisir un : ").strip())

    print(f"Bienvenue \033[91m{client.player_name}\033[0m !\n")
    print("Commandes disponibles : set_role, move<direction>, interact, get_game_state, quit")

    try:
        while True:
            user_input = input("Entrez une commande : ").strip().split()
            command = user_input[0]
            args = user_input[1:]

            if command == "quit":
                print("Fin du jeu.")
                break
            elif command == "start_game":
                client.game_started = True
                print("La partie commence !")
            elif command == "help":
                print("Commandes disponibles : set_role, move, interact, get_game_state, quit")
            else:
                client.execute_command(command, *args)
    except KeyboardInterrupt:
        print("\nDéconnexion.")
    finally:
        client.disconnect()
