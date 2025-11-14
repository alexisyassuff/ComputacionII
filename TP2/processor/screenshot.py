from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Maneja ChromeDriver automáticamente
import base64


def capture_webpage(request):
    url = request.get("url")
    if not url:
        return {"error": "No se proporcionó una URL para capturar el screenshot"}

    # Configuración de Selenium con Chrome
    options = Options()
    options.headless = True
    try:
        # Manejo de ChromeDriver automáticamente usando webdriver_manager
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

        # Abrir URL y capturar pantalla
        driver.get(url)
        screenshot_png = driver.get_screenshot_as_png()
        driver.quit()

        # Codificar captura en Base64
        screenshot_base64 = base64.b64encode(screenshot_png).decode("utf-8")
        return {"screenshot": screenshot_base64}
    except Exception as e:
        return {"error": f"Fallo al capturar screenshot: {str(e)}"}