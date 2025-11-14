from typing import Tuple, Optional
import aiohttp
import asyncio

# Valores por defecto
DEFAULT_LIMIT = 100          # max conexiones totales en el pool
DEFAULT_LIMIT_PER_HOST = 10  # max conexiones simultáneas por host


def make_session(limit: int = DEFAULT_LIMIT, limit_per_host: int = DEFAULT_LIMIT_PER_HOST, headers: dict | None = None) -> aiohttp.ClientSession:
    connector = aiohttp.TCPConnector(limit=limit, limit_per_host=limit_per_host)
    session = aiohttp.ClientSession(connector=connector, headers=headers)
    return session


async def fetch_text(session: aiohttp.ClientSession, url: str, timeout: int) -> Tuple[Optional[str], int, str]:
    try:
        timeout_cfg = aiohttp.ClientTimeout(total=timeout)
        async with session.get(url, timeout=timeout_cfg) as resp:
            resp.raise_for_status()  # lanza ClientResponseError si status >=400
            text = await resp.text()
            return text, resp.status, str(resp.url)
    except asyncio.TimeoutError as e:
        # Timeout: devolver None y un status simbólico (504)
        return None, 504, f"timeout: {e}"
    except aiohttp.ClientResponseError as e:
        # Respuesta con status 4xx/5xx
        return None, e.status, f"response_error: {e}"
    except aiohttp.InvalidURL as e:
        return None, 400, f"invalid_url: {e}"
    except Exception as e:
        # Errores de conexión, DNS, etc.
        return None, 502, f"connection_error: {e}"