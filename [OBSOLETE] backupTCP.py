import socket

def start_client():
       
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 9999))

        command = input("Position : ")
        client.send(command.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        print(response)
        if "La partie a commence !" in response:
            break
        client.close()

if __name__ == "__main__":
    start_client()



#------------------------------------------------------------------

import socket
import json

class GameClientTCP:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.role = None

    def send_request(self, request_data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.server_address, self.server_port))
                s.sendall(json.dumps(request_data).encode())
                response_data = s.recv(4096).decode()
                return json.loads(response_data)
        except Exception as e:
            print("Erreur lors de la communication avec le serveur :", e)
            return None

    def set_role(self, role):
        roles = ['villageois', 'vif d\'or', 'loup garou']
        if role not in roles:
            print("Erreur : Rôle invalide. Choisissez parmi :", roles)
            return
        request = {"action": "set_role", "role": role}
        response = self.send_request(request)
        if response and response.get("status") == "success":
            self.role = role
            print(f"Rôle attribué : {role}")
        else:
            print("Erreur lors de la définition du rôle :", response.get("error", "Erreur inconnue"))

    def move(self, direction):
        directions = ['north', 'south', 'east', 'west']
        if direction not in directions:
            print("Erreur : Direction invalide. Choisissez parmi :", directions)
            return
        request = {"action": "move", "direction": direction}
        response = self.send_request(request)
        if response and response.get("status") == "success":
            print("Déplacement effectué :", response.get("new_position"))
        else:
            print("Erreur lors du déplacement :", response.get("error", "Erreur inconnue"))

    def interact(self, object_name):
        request = {"action": "interact", "object_name": object_name}
        response = self.send_request(request)
        if response and response.get("status") == "success":
            print("Résultat de l'interaction :", response.get("result"))
        else:
            print("Erreur lors de l'interaction :", response.get("error", "Erreur inconnue"))

    def get_game_state(self):
        request = {"action": "get_state"}
        response = self.send_request(request)
        if response and response.get("status") == "success":
            print("Carte actuelle :", response.get("map"))
            print("Objets autour :", response.get("nearby_objects"))
            print("Temps restant :", response.get("time_remaining"))
        else:
            print("Erreur lors de la récupération de l'état :", response.get("error", "Erreur inconnue"))

    def run(self):
        while True:
            action = input("Choisissez une action (set_role, move, interact, get_state, quit): ").strip().lower()
            if action == "quit":
                print("Fermeture du client.")
                break
            elif action == "set_role":
                role = input("Entrez le rôle à attribuer (villageois, vif d'or, loup garou): ").strip().lower()
                self.set_role(role)
            elif action == "move":
                direction = input("Entrez une direction (north, south, east, west): ").strip().lower()
                self.move(direction)
            elif action == "interact":
                object_name = input("Entrez le nom de l'objet à interagir: ").strip()
                self.interact(object_name)
            elif action == "get_state":
                self.get_game_state()
            else:
                print("Action inconnue.")

if __name__ == "__main__":
    server_address = "localhost"  # Adresse du serveur
    server_port = 9999  # Port du serveur
    client = GameClientTCP(server_address, server_port)
    client.run()





#-----------------------------------------------------------------------

import socket
import json

def handle_client(client_socket):
    try:
        request_data = client_socket.recv(4096).decode()
        if not request_data:
            return
        
        request = json.loads(request_data)
        response = {"status": "error", "error": "Action non reconnue"}

        if request["action"] == "set_role":
            role = request.get("role", "")
            if role in ['villageois', 'vif d\'or', 'loup garou']:
                response = {"status": "success"}
            else:
                response = {"status": "error", "error": "Rôle invalide"}
        elif request["action"] == "move":
            direction = request.get("direction", "")
            if direction in ['north', 'south', 'east', 'west']:
                response = {"status": "success", "new_position": "x=10, y=20"}
            else:
                response = {"status": "error", "error": "Direction invalide"}
        elif request["action"] == "get_state":
            response = {
                "status": "success",
                "map": "Carte de test",
                "nearby_objects": ["arbre", "pierre"],
                "time_remaining": "5:00"
            }
        elif request["action"] == "interact":
            object_name = request.get("object_name", "")
            if object_name:
                response = {"status": "success", "result": f"Interaction réussie avec {object_name}"}
            else:
                response = {"status": "error", "error": "Objet non spécifié"}

        client_socket.sendall(json.dumps(response).encode())
    except Exception as e:
        print("Erreur serveur :", e)
        client_socket.sendall(json.dumps({"status": "error", "error": str(e)}).encode())
    finally:
        client_socket.close()

if __name__ == "__main__":
    server_address = "localhost"
    server_port = 9999

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_address, server_port))
    server_socket.listen(5)
    print(f"Serveur démarré sur {server_address}:{server_port}")

    while True:
        client_socket, addr = server_socket.accept()
        print("Connexion reçue de :", addr)
        handle_client(client_socket)
