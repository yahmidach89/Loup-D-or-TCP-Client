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