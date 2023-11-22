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
host = '127.0.0.1'
puerto = 55555  # Cambiar a un puerto diferente

# Crear un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al server
try:
    client_socket.connect((host, puerto))
except socket.error:
    print("Servidor no responde. Desconectando..")
    exit()

# Solicitar al usuario su nombre
try:
    name = input("Ingresa tu nombre: ")
except KeyboardInterrupt:
    exit()


if name.isalpha() or name.isdigit():
    #validar que sea nombre o numero

    try:
        full_message = f"{name} se ha Conectado"
        client_socket.send(full_message.encode('utf-8'))
    except KeyboardInterrupt:
        exit()
    # Enviar mensajes al servidor
    def sendMsj():
        while True:
            try:
                message = input()
                full_message = f"{name}: {message}"
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
    def getMSj():
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
        receive_h1 = threading.Thread(target=getMSj)

        # Iniciar un hilo para enviar mensajes del servidor
        send_h2 = threading.Thread(target=sendMsj)
        
        receive_h1.start()
        send_h2.start()

        receive_h1.join()
        send_h2.join()
    except (KeyboardInterrupt, SystemExit):
        exit()
    # Cerrar el socket después de salir del bucle
    client_socket.close()
else:
    print("Valor nombre o ID ingresado no valido!")
    client_socket.close()