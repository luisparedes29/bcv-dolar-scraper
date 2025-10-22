# Proyecto BCV - Extractor de Precio del Dólar

Este proyecto automatiza la extracción diaria del precio del dólar desde el sitio web del Banco Central de Venezuela (BCV) y lo guarda en un archivo JSON.

## Características

- ✅ Extracción automática del precio del dólar del BCV
- ✅ Guardado en archivo JSON con timestamp
- ✅ Logging detallado de todas las operaciones
- ✅ Múltiples métodos de búsqueda para mayor robustez
- ✅ Manejo de errores y reintentos
- ✅ Programación para ejecución diaria a las 6 PM

## Archivos del Proyecto

- `bcv_scraper.py` - Script principal de extracción
- `requirements.txt` - Dependencias de Python
- `ejecutar.bat` - Script de Windows para ejecución fácil
- `README.md` - Este archivo de documentación

## Instalación y Uso

### Método 1: Ejecución Automática (Recomendado)
1. Doble clic en `ejecutar.bat`
2. El script instalará las dependencias automáticamente
3. Ejecutará la extracción del precio del dólar

### Método 2: Ejecución Manual
1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecutar el script:
   ```bash
   python bcv_scraper.py
   ```

## Programación Automática (Tarea Diaria a las 6 PM)

### En Windows:
1. Abrir "Programador de tareas" (Task Scheduler)
2. Crear tarea básica
3. Configurar:
   - **Nombre**: "BCV Dólar Scraper"
   - **Frecuencia**: Diaria
   - **Hora**: 18:00 (6 PM)
   - **Acción**: Iniciar programa
   - **Programa**: `python`
   - **Argumentos**: `C:\Users\luis_\Desktop\ProyectoBCV\bcv_scraper.py`
   - **Directorio**: `C:\Users\luis_\Desktop\ProyectoBCV`

### En Linux/Mac:
```bash
# Editar crontab
crontab -e

# Agregar esta línea para ejecutar todos los días a las 6 PM:
0 18 * * * /usr/bin/python3 /ruta/completa/al/ProyectoBCV/bcv_scraper.py
```

## Archivos Generados

- `precio_dolar_bcv.json` - Archivo con todos los precios extraídos
- `bcv_scraper.log` - Log de todas las operaciones

## Estructura del JSON

```json
[
  {
    "fecha": "2024-01-15 18:00:00",
    "precio_dolar": 36.5,
    "timestamp": "2024-01-15T18:00:00.123456"
  }
]
```

## Solución de Problemas

### Error de conexión
- Verificar conexión a internet
- El sitio del BCV puede estar temporalmente fuera de servicio

### Error de dependencias
- Ejecutar: `pip install -r requirements.txt`

### Precio no encontrado
- El script incluye múltiples métodos de búsqueda
- Revisar el archivo `bcv_scraper.log` para más detalles

## Contacto

Para reportar problemas o sugerencias, revisar los logs en `bcv_scraper.log`.
