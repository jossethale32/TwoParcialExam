import tkinter as tk
from tkinter import ttk, messagebox
import socket

# Dirección y puerto del servidor
HOST = '127.0.0.1'
PORT = 12345  # Cambiar a un puerto diferente

# Crear un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Fact = """ """

# Conectar al servidor
try:
    client_socket.connect((HOST, PORT))
except socket.error:
    messagebox.showerror("Alerta", "No se puede Conectar con el servidor.")
    exit()

def updateFind(event):
    # print(str(len(entry_idcli.get())))
    if (len(entry_trama.get()) > 63):
        messagebox.showerror("Alerta", "Limite de Caracteres de ID es 63")
        entry_trama.delete(0, tk.END)
        entry_trama.insert(0, "")
        entry_trama.focus()

def close_win():
    root.destroy()

def disable_event():
    pass

def consulInfo():
    # Crear una ventana secundaria.
    ventana_secundaria.deiconify()
    ventana_secundaria.title("Consultar Informacion de Usuario")
    ventana_secundaria.config(width=1000, height=600)
    ventana_secundaria.protocol("WM_DELETE_WINDOW", disable_event)

    label_id = tk.Label(ventana_secundaria, text="#Trama: ")
    label_id.grid(row=1, column=0, pady=5)

    entry_trama.grid(row=1, column=1, pady=5)
    entry_trama.focus()

    boton_buscar = ttk.Button(
        ventana_secundaria,
        text="Obtener Info",
        command=subconsultar
    )
    
    boton_buscar.grid(row=1, column=2, pady=5)

    boton_cerrar = ttk.Button(
        ventana_secundaria,
        text="Cerrar ventana",
        command=ventana_secundaria.withdraw
    )

    boton_cerrar.grid(row=1, column=3, pady=5)

    T.insert(tk.END, Fact)
    T.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    entry_trama.bind('<KeyRelease>', updateFind)
    return id

def subconsultar():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 12345))
        # client_socket.settimeout(5)
        client_socket.send(str(entry_trama.get()).encode('utf-8'))
        texto = client_socket.recv(1024).decode('utf-8')
        T.delete('1.0', tk.END)
        T.insert(tk.END,texto)
        client_socket.close()
    except TimeoutError as e:
        messagebox.showerror("⚠️Error", "Servidor no Responde")
        # client_socket.close()
        response = ""
    except socket.timeout as ee:
        messagebox.showerror("⚠️Error", "Error de parte del servidor")
        # client_socket.close()
        response = ""
    except socket.error as e:
        messagebox.showerror("⚠️Error", "Verifica la Disponiblidad del servidor")
        quit()
    
    ventana_secundaria.update_idletasks()

# Interfaz gráfica de usuario con Tkinter
root = tk.Tk()
root.title("SocketInfo")

root.eval('tk::PlaceWindow . center')

# Botones
button_info = tk.Button(root, text="Consultar Información", command=consulInfo)
button_info.grid(row=0, column=0, padx=10, pady=10)

ventana_secundaria = tk.Toplevel()
ventana_secundaria.withdraw()
entry_trama = tk.Entry(ventana_secundaria)

ventana_secundariaP = tk.Toplevel()
ventana_secundariaP.withdraw()
entry_pago = tk.Entry(ventana_secundariaP)

ventana_secundariaP2 = tk.Toplevel()
ventana_secundariaP2.withdraw()

T = tk.Text(ventana_secundaria, height = 6, width = 72)

root.mainloop()