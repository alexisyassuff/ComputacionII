import multiprocessing as mp
import time
import random
from datetime import datetime
from analizador import ejecutar_analizador
from verificador import verificador_main

def crear_muestra(indice):
    muestra = {
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "frecuencia": random.randint(60, 180),
        "presion": [random.randint(110, 180), random.randint(70, 110)],
        "oxigeno": random.randint(90, 100)
    }
    # Cambios mínimos: cambia posición y valores de error respecto al original
    if indice == 12:
        muestra["frecuencia"] = 205
    if indice == 31:
        muestra["oxigeno"] = 87
    if indice == 50:
        muestra["presion"][0] = 202
    return muestra

if __name__ == "__main__":
    padre1, hijo1 = mp.Pipe()
    padre2, hijo2 = mp.Pipe()
    padre3, hijo3 = mp.Pipe()

    queue1 = mp.Queue()
    queue2 = mp.Queue()
    queue3 = mp.Queue()

    proc_verif = mp.Process(target=verificador_main, args=(queue1, queue2, queue3))
    proc_a = mp.Process(target=ejecutar_analizador, args=(hijo1, 'frecuencia', queue1))
    proc_b = mp.Process(target=ejecutar_analizador, args=(hijo2, 'presion', queue2))
    proc_c = mp.Process(target=ejecutar_analizador, args=(hijo3, 'oxigeno', queue3))

    proc_verif.start()
    proc_a.start()
    proc_b.start()
    proc_c.start()

    for i in range(60):
        muestra = crear_muestra(i)
        padre1.send(muestra)
        padre2.send(muestra)
        padre3.send(muestra)
        print(f"Enviada muestra {i+1}/60: {muestra}")
        time.sleep(1)

    padre1.send('FIN')
    padre2.send('FIN')
    padre3.send('FIN')
    proc_a.join()
    proc_b.join()
    proc_c.join()
    proc_verif.join()
    print("Todos los procesos terminaron correctamente.")