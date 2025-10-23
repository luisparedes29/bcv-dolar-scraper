# BCV Scraper - Versión Clean Code

Este proyecto ha sido refactorizado aplicando principios de **Clean Code** para mejorar la legibilidad, mantenibilidad y escalabilidad del código.

## 🎯 Mejoras Implementadas

### ✅ Principios de Clean Code Aplicados

1. **Funciones Pequeñas**: Cada función tiene una sola responsabilidad
2. **Nombres Descriptivos**: Variables y funciones con nombres claros y expresivos
3. **Eliminación de Duplicación**: Código reutilizable en módulos separados
4. **Separación de Responsabilidades**: Cada clase tiene un propósito específico
5. **Configuración Centralizada**: Todas las configuraciones en un solo lugar
6. **Manejo de Errores Robusto**: Logging detallado y manejo de excepciones
7. **Documentación Clara**: Docstrings y comentarios explicativos

## 📁 Estructura del Proyecto

```
ProyectoBCV/
├── bcv_scraper.py              # Script original
├── bcv_scraper_clean.py       # Versión refactorizada (intermedia)
├── bcv_scraper_final.py       # Versión final con Clean Code
├── config.py                  # Configuración centralizada
├── utils.py                   # Utilidades reutilizables
├── requirements.txt           # Dependencias
├── README_CleanCode.md        # Esta documentación
└── [archivos de datos y logs]
```

## 🏗️ Arquitectura Clean Code

### 1. **config.py** - Configuración Centralizada
```python
class ScraperConfig:
    BCV_URLS = [...]
    HTTP_HEADERS = {...}
    DATA_FILE = 'precio_dolar_bcv.json'
    # ... más configuraciones
```

### 2. **utils.py** - Utilidades Reutilizables
- `PriceParser`: Manejo de precios y conversiones
- `DateTimeUtils`: Utilidades de fecha y hora
- `TextUtils`: Procesamiento de texto
- `LogUtils`: Manejo de logging

### 3. **bcv_scraper_final.py** - Lógica Principal
- `WebClient`: Manejo de peticiones HTTP
- `DollarPriceFinder`: Extracción de precios
- `DataStorage`: Persistencia de datos
- `BCVDollarScraper`: Coordinador principal

## 🔧 Clases y Responsabilidades

### WebClient
- **Responsabilidad**: Hacer peticiones HTTP al BCV
- **Métodos principales**:
  - `fetch_page_content()`: Obtiene el HTML de la página

### DollarPriceFinder
- **Responsabilidad**: Encontrar el precio del dólar en el HTML
- **Estrategias de búsqueda**:
  - Div específico con id='dolar'
  - Texto que contenga palabras clave USD
  - Tablas HTML
  - Selectores CSS específicos

### DataStorage
- **Responsabilidad**: Guardar y cargar datos
- **Métodos principales**:
  - `save_dollar_price()`: Guarda precio en JSON
  - `_create_price_entry()`: Crea entrada con timestamp

### BCVDollarScraper
- **Responsabilidad**: Coordinar todo el proceso
- **Flujo**:
  1. Obtener contenido web
  2. Extraer precio
  3. Guardar datos

## 🚀 Cómo Usar

### Ejecución Simple
```bash
python bcv_scraper_final.py
```

### Ejecución con Batch (Windows)
```bash
ejecutar.bat
```

## 📊 Beneficios del Refactoring

### Antes (Script Original)
- ❌ Una clase gigante con múltiples responsabilidades
- ❌ Código duplicado en métodos de búsqueda
- ❌ Configuración hardcodeada
- ❌ Manejo de errores básico
- ❌ Difícil de testear y mantener

### Después (Clean Code)
- ✅ Clases pequeñas con responsabilidades específicas
- ✅ Código reutilizable y modular
- ✅ Configuración centralizada y flexible
- ✅ Manejo de errores robusto con logging detallado
- ✅ Fácil de testear, mantener y extender

## 🧪 Ventajas para Testing

La nueva estructura facilita las pruebas unitarias:

```python
# Ejemplo de test unitario
def test_price_parser():
    parser = PriceParser()
    assert parser.parse_price_to_float("36,50") == 36.50
    assert parser.parse_price_to_float("36.50") == 36.50
```

## 🔄 Extensibilidad

El código ahora es fácil de extender:

1. **Nuevas fuentes de datos**: Agregar nuevas URLs en `config.py`
2. **Nuevas estrategias de búsqueda**: Agregar métodos en `DollarPriceFinder`
3. **Nuevos formatos de almacenamiento**: Extender `DataStorage`
4. **Nuevas utilidades**: Agregar funciones en `utils.py`

## 📈 Preparación para Microservicio

Esta estructura está preparada para convertirse en un microservicio:

1. **Separación clara de responsabilidades** ✅
2. **Configuración externalizable** ✅
3. **Logging estructurado** ✅
4. **Manejo de errores robusto** ✅
5. **Código modular y testeable** ✅

## 🎯 Próximos Pasos

Para convertir en microservicio, se podría:

1. Agregar API REST con FastAPI/Flask
2. Containerizar con Docker
3. Agregar base de datos (PostgreSQL/MongoDB)
4. Implementar health checks
5. Agregar métricas y monitoreo

## 📝 Conclusión

El refactoring aplicando Clean Code ha resultado en:

- **Código más legible** y fácil de entender
- **Mejor mantenibilidad** y extensibilidad
- **Preparación para escalabilidad** como microservicio
- **Facilidad para testing** y debugging
- **Separación clara de responsabilidades**

El script mantiene toda su funcionalidad original pero ahora es mucho más profesional y preparado para crecer.
