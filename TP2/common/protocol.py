import asyncio
import json
import struct
from typing import Any, Dict

# Estructura para pack/unpack de 4 bytes big-endian (unsigned int)
MESSAGE_HEADER_FORMAT = struct.Struct("!I")  # network (= big-endian) unsigned int


async def exchange_data_with_engine(host: str, port: int, payload: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter

    # Serializar el payload a bytes UTF-8
    data = json.dumps(payload).encode("utf-8")
    length = len(data)
    if length > 10 * 1024 * 1024:
        # Protección básica: rechazar mensajes > 10MB (ajustable)
        raise ValueError("payload too large")

    # Abrir conexión asíncrona (non-blocking)
    reader, writer = await asyncio.open_connection(host, port)
    try:
        # Escribir prefijo de longitud + cuerpo
        writer.write(MESSAGE_HEADER_FORMAT.pack(length))
        writer.write(data)
        await writer.drain()  # asegurar que los bytes se envían al socket

        # Leer la respuesta: primero 4 bytes con la longitud
        raw = await asyncio.wait_for(reader.readexactly(4), timeout=timeout)
        (resp_len,) = MESSAGE_HEADER_FORMAT.unpack(raw)

        # Protección: no leer más de un límite razonable
        if resp_len > 50 * 1024 * 1024:
            # evitar leer mensajes absurdamente grandes
            raise ValueError("response too large")

        # Leer exactamente resp_len bytes (bloquea de forma asíncrona hasta recibirlos)
        body = await asyncio.wait_for(reader.readexactly(resp_len), timeout=timeout)
        # Decodificar JSON y devolver dict
        return json.loads(body.decode("utf-8"))
    finally:
        # Cerrar writer correctamente (await writer.wait_closed() en Python 3.7+)
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            # En shutdown / errores de red esto puede fallar; ignorar para no enmascarar el error original
            pass