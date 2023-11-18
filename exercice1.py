
#En siguiente Código describa como puede reconfigurar para que los hilos no afecten el incremento y de 
#la variable global y que vayan en secuencia. Realice los cambios en el Código para que se consuma 
#respectando la sección critica, haga que el counter vaya del valor a 0. 

import threading 
# variable global x inicializada a el valor 
x = 100000
lock = threading.Lock()             #implementar bloqueo threading

def decremento(): 
    global x
    with lock:                      #establecer un bloqueo de variable global
        x -= 1

def TareaThread(): 
    for _ in range(5000):           #como son 2 threads trabajando uno despues del otro el valor es 5000
        decremento()

def TareaPrin(): 
    global x 
    # creando hilos 
    t1 = threading.Thread(target=TareaThread) 
    t2 = threading.Thread(target=TareaThread) 
    # inicio de los hilos 
    t1.start() 
    t2.start() 
    # uniendo hilos 
    t1.join() 
    t2.join()

if __name__ == "__main__": 
    for i in range(10): 
        TareaPrin() 
        print("Iteraccion {0}: x = {1}".format(i, x)) 