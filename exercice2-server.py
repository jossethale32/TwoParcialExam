import socket
import threading
import datetime


# Configura el servidor de sockets
addr='127.0.0.1'
port=12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
paisCods=['01','02','03','00']
resp=""

try:
    server_socket.bind((addr, port))
    server_socket.listen(5)
except socket.error as tt:
    print("Error-Ya Existe un Servidor corriendo sobre este puerto ("+str(port)+")")
    server_socket.close()
    quit()

# Función para manejar las conexiones de los clientes
def handle_client(client_socket, addr):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')     #DATA OBTENIDA DEL CLIENTE
            if not data:
                break
            client_socket.send(validarData(data).encode('utf-8'))
        except socket.timeout as erroT:
            print(erroT)
            break
        except Exception as erro:
            print(erro)
            break
    client_socket.close()

#Validar info para parsear
def validarData(entrada):
    codpais=entrada[0:2]
    edad=entrada[2:4]
    genero=entrada[4:5]
    fechanac=entrada[5:13]
    nombreC=entrada[13:62]

    invalidados=0
    paisEncontrado=""
    if codpais.isdigit() and invalidados==0:
        encontrado=0
        for cod in paisCods:
            if str(codpais) == str(cod):
                encontrado=1

        if encontrado==0:
            invalidados=1
        elif encontrado==1:
            if str(codpais) == "01": paisEncontrado="Honduras"
            elif str(codpais) == "02": paisEncontrado="Costa Rica"
            elif str(codpais) == "03": paisEncontrado="México"
            elif str(codpais) == "00": paisEncontrado="País Desconocido"
    else:
        invalidados=1

    edadState=""
    if edad.isdigit() and invalidados==0:
        if int(edad)<=0:
            invalidados=1
        if int(edad)>=1 and int(edad)<=18:
            edadState="Menor de Edad"
        elif int(edad)>=19 and int(edad)<=50:
             edadState="Adulto"
        elif int(edad)>=51:
             edadState="Tercera Edad"
    else:
        invalidados=1
    
    
    if genero.isalpha() and invalidados==0:
        encontradog=0
        if str(genero).lower()=="m":
            encontradog=1
        elif str(genero).lower()=="f":
            encontradog=1
        else:
            encontradog=0
        if encontrado==0:
            invalidados=1

    noconcuerda=1
    fechafix=""
    frase=""
    if fechanac.isdigit() and invalidados==0:
        if len(fechanac)>0:
            #FECHA ACTUAL
            today = datetime.date.today()
            year = today.year

            #PARSEO DE FECHA
            ano=int(fechanac[0:4])
            mes=int(fechanac[4:6])
            dia=int(fechanac[6:8])

            fechafix=""+str(dia)+"-"+str(mes)+"-"+str(ano)

            fechaCalculada=year-ano

            if str(genero).lower()=="m":
                if int(edad)>=1 and int(edad)<=18:
                    frase="un niño menor de edad"
                elif int(edad)>=19 and int(edad)<=50:
                    frase="un joven adulto "
                elif int(edad)>=51:
                    frase="un adulto mayor edad"
            elif str(genero).lower()=="f":
                if int(edad)>=1 and int(edad)<=18:
                    frase="una niña menor de edad"
                elif int(edad)>=19 and int(edad)<=50:
                    frase="una joven adulto"
                elif int(edad)>=51:
                    frase="una mujer mayor de edad"
            if ano<=year:           #fecha dentro del rango(año)
                if fechaCalculada != int(edad):
                    noconcuerda=1
                elif fechaCalculada == int(edad):
                    noconcuerda=0
            elif ano>=year:         #fecha invalida(año)
                invalidados=1
    else:
        invalidados=1

    if nombreC.replace(' ','').isalpha() and invalidados==0:
        if len(nombreC)>0:
            palabras = nombreC.split()
            if len(palabras) <=1:
                invalidados=1
    else:
        invalidados=1

    if invalidados==1:
        return "....Algo Fallo....\nREVISA TU TRAMA DE ENTRADA!"
    else:
        if noconcuerda==1:
            return f"Hola {nombreC}, veo que eres del país de {paisEncontrado} y tienes {edad} años, lo que indica que eres {frase}. Sin embargo, al observar tu fecha de nacimiento ({fechafix}), noto que la edad no concuerda con la fecha de nacimiento."
        else:
            return f"Hola {nombreC}, veo que eres del país de {paisEncontrado} y tienes {edad} años, lo que indica que eres {frase}. Veo que tu fecha de Nacimiento concuerda con tu edad ({fechafix})"
# Metodo para iniciar el servidor de sockets
def start_server():
    print("Servidor Iniciado...\nEsperando Conexion...")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            # print(f"Cliente conectado: {addr} ")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_handler.start()
        except KeyboardInterrupt:
            server_socket.close()
            break
        except Exception as ee:
            print(ee)

# Inicia el servidor de sockets
start_server()