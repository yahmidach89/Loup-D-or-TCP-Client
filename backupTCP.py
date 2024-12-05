import socket
import json

class GameClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.role = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Connect to the game server using a socket."""
        self.client_socket.connect((self.server_host, self.server_port))

    def send_command(self, command):
        """Send a command to the server and receive the response."""
        self.client_socket.send(command.encode('utf-8'))
        response = self.client_socket.recv(1024).decode('utf-8')
        return response

    def set_role(self, role):
        roles = ['villageois', 'vif d\'or', 'loup garou']
        if role not in roles:
            print("Erreur : Rôle invalide. Choisissez parmi :", roles)
            return
        command = json.dumps({"action": "set_role", "role": role})
        response = self.send_command(command)
        if "Rôle attribué" in response:
            self.role = role
            print(f"Rôle attribué : {role}")
        else:
            print("Erreur lors de la définition du rôle :", response)

    def move(self, direction):
        directions = ['north', 'south', 'east', 'west']
        if direction not in directions:
            print("Erreur : Direction invalide. Choisissez parmi :", directions)
            return
        command = json.dumps({"action": "move", "direction": direction})
        response = self.send_command(command)
        if "Déplacement effectué" in response:
            print("Déplacement effectué :", response)
        else:
            print("Erreur lors du déplacement :", response)

    def interact(self, object_name):
        command = json.dumps({"action": "interact", "object_name": object_name})
        response = self.send_command(command)
        if "Résultat de l'interaction" in response:
            print("Résultat de l'interaction :", response)
        else:
            print("Erreur lors de l'interaction :", response)

    def get_game_state(self):
        command = json.dumps({"action": "get_game_state"})
        response = self.send_command(command)
        if response:
            try:
                data = json.loads(response)
                print("Carte actuelle :", data.get("map"))
                print("Objets autour :", data.get("nearby_objects"))
                print("Temps restant :", data.get("time_remaining"))
            except json.JSONDecodeError:
                print("Erreur lors de la récupération de l'état :", response)
        else:
            print("Erreur lors de la récupération de l'état.")

def start_client():
    server_host = "localhost"
    server_port = 9999
    client = GameClient(server_host, server_port)

    client.connect()
    print("Connecté au serveur de jeu.")

    while True:
        command = input("Entrez une commande : ")

        if command == "exit":
            print("Déconnexion du serveur.")
            client.client_socket.close()
            break

        elif command.startswith("role "):
            role = command.split(" ", 1)[1]
            client.set_role(role)

        elif command.startswith("move "):
            direction = command.split(" ", 1)[1]
            client.move(direction)

        elif command.startswith("interact "):
            object_name = command.split(" ", 1)[1]
            client.interact(object_name)

        elif command == "state":
            client.get_game_state()

        else:
            print("Commande inconnue. Essayez 'role <rôle>', 'move <direction>', 'interact <objet>', ou 'state'.")

if __name__ == "__main__":
    start_client()
