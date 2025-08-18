import hashlib
import json

def hash_sha256_hex(texto):
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()

def verificador_main(queue_f, queue_p, queue_o):
    blockchain = []
    hash_previo = '0' * 64
    for bloque_idx in range(60):
        res_f = queue_f.get()
        res_p = queue_p.get()
        res_o = queue_o.get()
        datos = {
            res_f['tipo']: {
                "media": res_f['prom'],
                "desv": res_f['desv'],
                "ultimo": res_f['valor_actual']
            },
            res_p['tipo']: {
                "media": res_p['prom'],
                "desv": res_p['desv'],
                "ultimo": res_p['valor_actual']
            },
            res_o['tipo']: {
                "media": res_o['prom'],
                "desv": res_o['desv'],
                "ultimo": res_o['valor_actual']
            }
        }
        # Validaciones con prints diferentes
        alerta = (
            datos['frecuencia']['media'] > 200 or
            datos['frecuencia']['ultimo'] > 200 or
            not (90 <= datos['oxigeno']['media'] <= 100) or
            not (90 <= datos['oxigeno']['ultimo'] <= 100) or
            datos['presion']['media'] > 200 or
            datos['presion']['ultimo'] > 200
        )
        momento = res_f['momento']
        bloque = {
            "timestamp": momento,
            "datos": datos,
            "alerta": alerta,
            "previo": hash_previo
        }
        bloque_str = str(bloque['previo']) + str(bloque['datos']) + bloque['timestamp']
        bloque_hash = hash_sha256_hex(bloque_str)
        bloque['hash'] = bloque_hash
        blockchain.append(bloque)
        hash_previo = bloque_hash
        print(f"-- Bloque {bloque_idx+1}: Hash {bloque_hash} | ALERTA: {'Sí' if alerta else 'No'}")
        with open("blockchain.json", "w") as archivo:
            json.dump(blockchain, archivo, indent=2)
    print("Verificación y almacenamiento de la cadena completa.")
