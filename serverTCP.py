import socket
import json
import threading

class GameServer:
    def __init__(self, host="localhost", port=9999):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}  # Dictionnaire pour stocker les informations des joueurs
        self.game_state = {
            "game_started": False,
            "map": "Une carte par défaut",
            "objects": ["épée", "bouclier", "potion"],
            "players": {}
        }
        self.lock = threading.Lock()  # Pour la synchronisation entre threads

    def start(self):
        """Démarre le serveur."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Serveur démarré sur {self.host}:{self.port}")

        try:
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"Connexion acceptée depuis {address}")
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        except KeyboardInterrupt:
            print("\nArrêt du serveur.")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        """Gère la communication avec un client."""
        try:
            while True:
                request = client_socket.recv(4096).decode()
                if not request:
                    break

                # Analyse de la requête JSON
                try:
                    data = json.loads(request)
                    action = data.get("action")
                    payload = data.get("payload", {})
                    response = self.handle_action(action, payload)
                except json.JSONDecodeError:
                    response = {"status": "error", "message": "Requête invalide."}

                # Envoi de la réponse au client
                client_socket.sendall(json.dumps(response).encode())
        except Exception as e:
            print(f"Erreur avec un client : {e}")
        finally:
            client_socket.close()

    def handle_action(self, action, payload):
        """Gère une action envoyée par un client."""
        with self.lock:  # Protection contre les accès concurrents
            if action == "set_role":
                return self.set_role(payload)
            elif action == "move":
                return self.move(payload)
            elif action == "interact":
                return self.interact(payload)
            elif action == "get_game_state":
                return self.get_game_state(payload)
            else:
                return {"status": "error", "message": f"Action '{action}' non reconnue."}

    def set_role(self, payload):
        """Attribue un rôle à un joueur."""
        player_name = payload.get("player_name")
        role = payload.get("role")
        if not player_name or not role:
            return {"status": "error", "message": "Nom du joueur ou rôle manquant."}

        roles = ['villageois', 'vif d\'or', 'loup garou']
        if role not in roles:
            return {"status": "error", "message": f"Rôle invalide. Choisissez parmi : {roles}"}

        if player_name not in self.game_state["players"]:
            self.game_state["players"][player_name] = {"role": None, "position": (0, 0)}

        self.game_state["players"][player_name]["role"] = role
        return {"status": "success", "message": f"Rôle '{role}' attribué à {player_name}."}

    def move(self, payload):
        """Déplace un joueur dans une direction donnée."""
        player_name = payload.get("player_name")
        direction = payload.get("direction")
        if not player_name or not direction:
            return {"status": "error", "message": "Nom du joueur ou direction manquante."}

        if not self.game_state["game_started"]:
            return {"status": "error", "message": "La partie n'a pas encore commencé."}

        player = self.game_state["players"].get(player_name)
        if not player:
            return {"status": "error", "message": "Joueur non trouvé."}

        x, y = player["position"]
        if direction == "NORTH":
            y += 1
        elif direction == "SOUTH":
            y -= 1
        elif direction == "EAST":
            x += 1
        elif direction == "WEST":
            x -= 1
        else:
            return {"status": "error", "message": "Direction invalide."}

        self.game_state["players"][player_name]["position"] = (x, y)
        return {"status": "success", "new_position": (x, y)}

    def interact(self, payload):
        """Permet à un joueur d'interagir avec un objet."""
        player_name = payload.get("player_name")
        object_name = payload.get("object_name")
        if not player_name or not object_name:
            return {"status": "error", "message": "Nom du joueur ou objet manquant."}

        if object_name not in self.game_state["objects"]:
            return {"status": "error", "message": f"L'objet '{object_name}' n'existe pas."}

        # Simuler une interaction
        return {"status": "success", "result": f"Vous avez interagi avec '{object_name}'."}

    def get_game_state(self, payload):
        """Retourne l'état actuel de la partie."""
        player_name = payload.get("player_name")
        if not player_name:
            return {"status": "error", "message": "Nom du joueur manquant."}

        player = self.game_state["players"].get(player_name)
        if not player:
            return {"status": "error", "message": "Joueur non trouvé."}

        return {
            "status": "success",
            "data": {
                "game_started": self.game_state["game_started"],
                "map": self.game_state["map"],
                "nearby_objects": self.game_state["objects"],
                "time_remaining": "5 minutes"
            }
        }

if __name__ == "__main__":
    server = GameServer()
    server.start()
