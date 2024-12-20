import socket
import requests

class GameClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.role = None

    def set_role(self, role):
        roles = ['villageois', 'vif d\'or', 'loup garou']
        if role not in roles:
            print("Erreur : Rôle invalide. Choisissez parmi :", roles)
            return
        response = requests.post(f"{self.server_url}/set_role", json={"role": role})
        if response.status_code == 200:
            self.role = role
            print(f"Rôle attribué : {role}")
        else:
            print("Erreur lors de la définition du rôle :", response.text)

    def move(self, direction):
        directions = ['north', 'south', 'east', 'west']
        if direction not in directions:
            print("Erreur : Direction invalide. Choisissez parmi :", directions)
            return
        response = requests.post(f"{self.server_url}/move", json={"direction": direction})
        if response.status_code == 200:
            data = response.json()
            print("Déplacement effectué :", data.get("new_position"))
        else:
            print("Erreur lors du déplacement :", response.text)

    def interact(self, object_name):
        response = requests.post(f"{self.server_url}/interact", json={"object_name": object_name})
        if response.status_code == 200:
            data = response.json()
            print("Résultat de l'interaction :", data.get("result"))
        else:
            print("Erreur lors de l'interaction :", response.text)

    def get_game_state(self):
        response = requests.get(f"{self.server_url}/state")
        if response.status_code == 200:
            data = response.json()
            print("Carte actuelle :", data.get("map"))
            print("Objets autour :", data.get("nearby_objects"))
            print("Temps restant :", data.get("time_remaining"))
        else:
            print("Erreur lors de la récupération de l'état :", response.text)

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
