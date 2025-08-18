import numpy as np

def ejecutar_analizador(canal, tipo_senal, resultado_queue):
    ventana_datos = []
    while True:
        paquete = canal.recv()
        if paquete == 'FIN':
            print(f"[{tipo_senal}] Proceso finalizado.")
            break
        # Selección de la señal correspondiente
        if tipo_senal == 'frecuencia':
            dato = paquete['frecuencia']
        elif tipo_senal == 'presion':
            dato = paquete['presion'][0]
        elif tipo_senal == 'oxigeno':
            dato = paquete['oxigeno']
        else:
            print("Tipo no reconocido")
            continue
        ventana_datos.append(dato)
        if len(ventana_datos) > 30:
            ventana_datos.pop(0)
        # Estadísticas
        promedio = float(np.mean(ventana_datos))
        desviacion = float(np.std(ventana_datos))
        resultado = {
            "tipo": tipo_senal,
            "momento": paquete['timestamp'],
            "prom": promedio,
            "desv": desviacion,
            "valor_actual": dato
        }
        resultado_queue.put(resultado)
        print(f"[{tipo_senal}] Resultado enviado: media={promedio:.2f}, desv={desviacion:.2f}")