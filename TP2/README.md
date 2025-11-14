# TP2 - Sistema de Scraping y Análisis Web Distribuido

Sistema distribuido de dos servidores que procesa páginas web de forma asíncrona y paralela. El Servidor A maneja las peticiones HTTP y scraping, mientras que el Servidor B se encarga del procesamiento computacional intensivo.

## Arquitectura del Sistema

### Componentes Principales

- **Servidor de Scraping** (`server_scraping.py`): Servidor asyncio que maneja peticiones HTTP y extracción de datos
- **Servidor de Procesamiento** (`server_processing.py`): Servidor multiprocessing para tareas computacionalmente intensivas
- **Cliente de Prueba** (`client.py`): Herramienta para validar el funcionamiento completo del sistema

### Módulos de Soporte

````
common/              # Protocolo de comunicación entre servidores
├── protocol.py          # Intercambio de mensajes JSON binarios
└── serialization.py     # Codificación y serialización de datos

scraper/             # Extracción y análisis de contenido web
├── html_parser.py       # Parsing HTML con BeautifulSoup
├── async_http.py        # Cliente HTTP asíncrono
└── metadata_extractor.py # Extracción de metadatos web

processor/           # Procesamiento computacional intensivo
├── screenshot.py        # Capturas de pantalla con Selenium
├── performance.py       # Análisis de métricas de rendimiento
└── image_processor.py   # Procesamiento de imágenes

tests/               # Validación y pruebas del sistema
├── test_scraper.py      # Tests de módulos de scraping
└── test_processor.py    # Tests de módulos de procesamiento
```## Instalación y Configuración

### Dependencias

```bash
# Crear y activar entorno virtual
python -m venv venv_tp2
source venv_tp2/bin/activate  # Linux/Mac
# o: venv_tp2\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
````

## Ejecución del Sistema

### Paso 1: Iniciar Servidor de Procesamiento (Parte B)

```bash
source venv_tp2/bin/activate && python server_processing.py -i 127.0.0.1 -p 9001 -n 1
```

**Parámetros:**

- `-i`: Dirección IP de escucha
- `-p`: Puerto de escucha
- `-n`: Número de procesos en el pool (según enunciado)

### Paso 2: Iniciar Servidor de Scraping (Parte A)

```bash
source venv_tp2/bin/activate && python server_scraping.py -i 127.0.0.1 -p 8000 -w 2 --engine-host 127.0.0.1 --engine-port 9001
```

**Parámetros:**

- `-i`: Dirección IP de escucha (soporta IPv4/IPv6)
- `-p`: Puerto HTTP de escucha
- `-w`: Número de workers (según enunciado)
- `--engine-host`: IP del servidor de procesamiento
- `--engine-port`: Puerto del servidor de procesamiento

### Paso 3: Probar el Sistema Completo

```bash
source venv_tp2/bin/activate && python3 client.py --url https://www.google.com
```

## Funcionalidades Implementadas

### Extracción de Datos Web

- **Título de página**: Extracción automática del tag `<title>`
- **Enlaces**: Recolección de todos los links con normalización de URLs
- **Metadatos**: Tags meta, Open Graph y Schema.org
- **Estructura HTML**: Conteo de headers H1-H6
- **Análisis de imágenes**: Conteo total de elementos `<img>`

### Procesamiento Avanzado

- **Screenshots**: Captura PNG de páginas renderizadas
- **Métricas de rendimiento**: Tiempo de carga, tamaño de recursos, número de requests
- **Análisis visual**: Generación de thumbnails optimizados
- **Procesamiento paralelo**: Utiliza multiprocessing para tareas CPU-intensivas

### Comunicación Entre Servidores

- **Protocolo binario**: Messages length-prefixed con serialización JSON
- **Comunicación asíncrona**: El Servidor A no bloquea mientras espera respuestas
- **Manejo de errores**: Timeouts, reconexiones y fallos de red
- **Transparencia**: El cliente solo interactúa con el Servidor A

## Formato de Respuesta

El sistema devuelve un JSON estructurado:

```json
{
  "target_url": "https://ejemplo.com",
  "analysis_timestamp": "2025-11-14T16:19:05Z",
  "extraction_results": {
    "title": "Título de la página",
    "links": ["url1", "url2"],
    "meta_tags": {
      "viewport": "width=device-width, initial-scale=1"
    },
    "structure": {
      "h1": 1,
      "h2": 3,
      "h3": 0
    },
    "images_count": 5
  },
  "computation_results": {
    "status": "success",
    "processing_data": {
      "screenshot": "data:image/png;base64,iVBOR...",
      "performance": {
        "load_time_ms": 807,
        "total_size_kb": 1024,
        "num_requests": 12
      },
      "thumbnails": []
    }
  },
  "operation_status": "completed"
}
```

## Tecnologías Utilizadas

### Servidor A (Asíncrono)

- **aiohttp**: Framework web asíncrono
- **asyncio**: Programación concurrente no bloqueante
- **BeautifulSoup**: Parsing HTML robusto
- **aiofiles**: I/O de archivos asíncrono

### Servidor B (Paralelo)

- **multiprocessing**: Procesamiento paralelo real
- **socketserver**: Manejo de conexiones TCP
- **Selenium**: Automatización de navegador
- **Pillow**: Procesamiento de imágenes

### Comunicación

- **JSON**: Serialización de mensajes
- **TCP Sockets**: Comunicación confiable entre procesos
- **Protocol Buffers**: Intercambio binario eficiente

## Características Técnicas

### Concurrencia

- **Servidor A**: Maneja múltiples clientes simultáneamente usando asyncio
- **Servidor B**: Procesa tareas en paralelo usando un pool de procesos
- **Límites configurables**: Control de carga mediante semáforos

### Rendimiento

- **Scraping asíncrono**: No bloquea el event loop principal
- **Cache de conexiones**: Reutilización de conexiones HTTP
- **Procesamiento en background**: Tareas CPU-intensivas no afectan la responsividad

## Solución de Problemas

### Servidor no inicia

```bash
# Verificar puertos en uso
netstat -tlnp | grep -E "8000|9001"

# Liberar puertos si es necesario
pkill -f server_scraping.py
pkill -f server_processing.py
```

### Fallos de screenshot

```bash
# Verificar instalación de Chrome
which google-chrome

# Instalar dependencias de sistema
sudo apt-get install -y chromium-browser
```

### Errores de conexión

```bash
# Verificar conectividad
curl http://127.0.0.1:8000/health

# Comprobar logs del servidor
tail -f server_a.log
```

---

**Desarrollado como parte del TP2 - Computación II**
