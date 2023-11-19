# Desarrolla un servidor de sockets que permita enviar mensajes de difusión (broadcast) a todos los 
# clientes conectados. La funcionalidad debe ser diseñada de manera que cuando un cliente envíe un 
# mensaje al servidor, este mensaje se retransmita a todos los demás clientes conectados. 

# Indica la lógica de broadcast en el servidor.  
# ¿Qué estructuras de datos o mecanismos utilizarías para almacenar y administrar las conexiones de 
# los clientes?  
# Proporciona una breve explicación del flujo de trabajo en el servidor para gestionar y difundir 
# mensajes a todos los clientes. 
# Además, considera cómo manejarías situaciones como la desconexión de un cliente y cómo 
# notificarías a los demás clientes sobre estas desconexiones. 

import socket
import threading
import sys

# Dirección y puerto del servidor
HOST = '127.0.0.1'
PORT = 55556

# Crear un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlace del socket al host y puerto
try:
    server_socket.bind((HOST, PORT))
except socket.error:
    print("Servidor no puede iniciarse")
    exit()
except Exception:
    print("Servidor no puede iniciarse")
    exit()
# Escuchar conexiones entrantes
server_socket.listen()

# Lista para almacenar las conexiones de los clientes
clients = []

# Función para enviar mensajes de difusión a todos los clientes
def broadcast(message, sender_socket=None):
    encoded_message = message.encode('utf-8')  # Codificar el mensaje a bytes
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(encoded_message)
            except socket.error:
                clients.remove(client_socket)

# Función para manejar la conexión con cada cliente
def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            mensajeDecode = message.decode('utf-8').lower()
            if "adios" in mensajeDecode:
                message2 = mensajeDecode.split(':') 
                # Enviar mensaje de despedida a los demás clientes
                broadcast(f"{client_address} - {message2[0]} se ha desconectado.", client_socket)
                print(f"{client_address} - {message2[0]} se ha desconectado.")
                # Cerrar el socket del cliente
                clients.remove(client_socket)
                break
            broadcast(f"[{client_address}] {message.decode('utf-8')}", client_socket)
            print(f"{client_address} - {message.decode('utf-8')}")
            
        except socket.error:
            clients.remove(client_socket)
            break
    
# Metodo de Difusion de mensajes desde el servidor
def difusion():
    while True:
        if len(clients) > 0:
            try:
                re=input("")
                if len(re) > 0:
                    for cliente in clients:
                        try:
                            cliente.send(str(re).encode('utf-8'))
                        except:
                            clients.remove(cliente)
            except Exception:
                print ("Sesion Terminada.")
                break


# Ciclo principal para aceptar conexiones de clientes
print("....SERVIDOR ACTIVO.... port:55556")
while True:
    try:
        # Aceptar una nueva conexión
        client_socket, addr = server_socket.accept()
        # print(f"Conexión establecida desde {addr}")

        # Agregar el socket del cliente a la lista
        clients.append(client_socket)

        # Iniciar un hilo para manejar la conexión con el cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

        # Iniciar un hilo para despues que cada cliente se conecte para envio de mensajes en difucion a todos ellos
        difusiont = threading.Thread(target=difusion)
        difusiont.start()

    except KeyboardInterrupt:
        exit()
        break
        False
    