# Sistema Concurrente de Análisis Biométrico con Cadena de Bloques Local

## Requisitos

- Python 3.9 o superior
- numpy

### Instalación de dependencias

Se recomienda usar un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

1. Ejecuta el programa principal para generar la cadena de bloques:

   ```bash
   python main.py
   ```

   Esto creará el archivo `blockchain.json` tras unos 60 segundos

2. Ejecuta el verificador para analizar la cadena y generar el reporte:

   ```bash
   python verificar_cadena.py
   ```

   Esto creará el archivo `reporte.txt` con los resultados

## Archivos generados

- `blockchain.json`: Contiene la cadena de bloques de todas las muestras
- `reporte.txt`: Resumen con cantidad de bloques, bloques corruptos, alertas y promedios
