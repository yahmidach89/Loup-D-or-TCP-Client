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
