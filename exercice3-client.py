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
import requests

# Dirección y puerto del servidor
HOST = '127.0.0.1'
PORT = 55556  # Cambiar a un puerto diferente

# Crear un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
try:
    client_socket.connect((HOST, PORT))
except socket.error:
    print("Servidor no responde. Desconectando.")
    exit()

# Solicitar al usuario que ingrese un nombre o identificación única
client_name = input("Ingresa tu nombre: ")

if client_name.isalpha() or client_name.isdigit():
    try:
        full_message = f"{client_name} se ha Conectado"
        client_socket.send(full_message.encode('utf-8'))
    except KeyboardInterrupt:
        exit()
    # Enviar mensajes al servidor
    def send_messages():
        while True:
            try:
                message = input()
                full_message = f"{client_name}: {message}"
                client_socket.send(full_message.encode('utf-8'))

                # Si el usuario escribe "adios", cerrar el cliente
                if message.lower() == "adios":
                    break
            except KeyboardInterrupt:
                exit()
            except socket.error:
                print("Error al recibir mensajes. Desconectando.")
                client_socket.close()
                break
            except Exception:
                print("Error al recibir mensajes. Desconectando.")
                client_socket.close()
                break

    # Función para recibir mensajes del servidor
    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                print(message)
            except socket.error:
                print("Error al recibir mensajes. Desconectando.")
                client_socket.close()
                break
    
    try:
        # Iniciar un hilo para recibir mensajes del servidor
        receive_thread = threading.Thread(target=receive_messages)

        # Iniciar un hilo para enviar mensajes del servidor
        send_thread = threading.Thread(target=send_messages)
        
        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()
    except (KeyboardInterrupt, SystemExit):
        exit()
    # Cerrar el socket después de salir del bucle
    client_socket.close()
else:
    print("Valor ingresado no valido!")
    client_socket.close()