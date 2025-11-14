from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import time
from urllib.parse import urlparse


def analyze_performance(request):
    url = request.get("url")
    if not url:
        return {"error": "No se proporcionó una URL para analizar el rendimiento"}

    options = Options()
    options.headless = True  # Ejecutar en modo headless (sin GUI)
    options.add_argument("--remote-debugging-port=9222")  # Necesario para habilitar CDP

    driver = webdriver.Chrome(service=Service(), options=options)
    driver.set_page_load_timeout(30)  # Timeout máximo para cargar la página

    try:
        # Habilitamos el Performance Logging usando CDP (Chrome DevTools Protocol)
        driver.execute_cdp_cmd("Performance.enable", {})

        # Medir tiempo de carga
        start_time = time()
        driver.get(url)
        load_time_ms = (time() - start_time) * 1000  # Convertimos a milisegundos

        # Obtener eventos de rendimiento desde el navegador
        performance_logs = driver.execute_cdp_cmd("Performance.getMetrics", {})
        network_logs = driver.get_log("performance")  # Otra forma de capturar logs brutos

        # Calcular tamaño total de recursos descargados (network traffic)
        total_size_kb = 0
        num_requests = 0
        for log in network_logs:
            try:
                # Filtrar eventos de "Network.responseReceived"
                message = log["message"]
                if "Network.responseReceived" in message:
                    num_requests += 1  # Contamos cada solicitud HTTP
                if "Network.loadingFinished" in message:
                    size_info = log["params"]["encodedDataLength"]
                    total_size_kb += int(size_info) / 1024  # Convertir bytes -> KB
            except KeyError:
                continue

        driver.quit()

        # Retornar métricas completas
        return {
            "performance": {
                "url": url,
                "domain": urlparse(url).netloc,  # Dominios que se consultaron
                "load_time_ms": round(load_time_ms, 2),
                "total_size_kb": round(total_size_kb, 2),
                "num_requests": num_requests,
            }
        }
    except Exception as e:
        driver.quit()
        return {"error": f"Ocurrió un error al analizar la URL: {str(e)}"}