import json
import hashlib

def hash_sha256_hex(texto):
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()

with open("blockchain.json", "r") as arch:
    bloques = json.load(arch)

corruptos = []
total_alertas = 0
suma_frec = 0
suma_pres = 0
suma_oxi = 0

for idx, bloque in enumerate(bloques):
    prev = bloque['previo']
    datos = bloque['datos']
    ts = bloque['timestamp']
    bloque_str = str(prev) + str(datos) + ts
    hash_actual = hash_sha256_hex(bloque_str)
    if bloque['hash'] != hash_actual:
        corruptos.append(str(idx))
    if bloque.get("alerta"):
        total_alertas += 1
    suma_frec += datos['frecuencia']['media']
    suma_pres += datos['presion']['media']
    suma_oxi += datos['oxigeno']['media']

total_bloques = len(bloques)

with open("reporte.txt", "w") as f:
    f.write(f"Cantidad total de bloques: {total_bloques}\n")
    f.write(f"Bloques corruptos: {', '.join(corruptos) if corruptos else '0'}\n")
    f.write(f"Bloques con alerta: {total_alertas}\n")
    f.write(f"Promedio frecuencia: {suma_frec/total_bloques:.2f}\n")
    f.write(f"Promedio presión: {suma_pres/total_bloques:.2f}\n")
    f.write(f"Promedio oxígeno: {suma_oxi/total_bloques:.2f}\n")
print("Reporte generado correctamente.")