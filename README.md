# 🇻🇪 BCV Dólar Scraper

**Extractor automático del precio del dólar del Banco Central de Venezuela (BCV)**

Este proyecto automatiza la extracción diaria del precio del dólar desde el sitio web del BCV y lo almacena en un archivo JSON con timestamps precisos y lógica de fechas correcta.

## ✨ Características Principales

- 🎯 **Extracción Automática**: Obtiene el precio del dólar del BCV automáticamente
- 📅 **Lógica de Fechas Inteligente**: Distingue entre fecha de extracción y fecha del precio
- 🔄 **Múltiples Paradigmas**: Versiones funcional, OOP y Clean Code
- 📊 **Almacenamiento JSON**: Historial completo con timestamps
- 🛡️ **Robusto**: Múltiples estrategias de búsqueda y manejo de errores
- 📝 **Logging Detallado**: Registro completo de todas las operaciones
- ⚡ **Fácil Uso**: Scripts de ejecución automática
- 📧 **Notificaciones**: Soporte para email y Telegram
- 🔧 **Configuración Centralizada**: Gestión fácil de parámetros

## 🏗️ Arquitectura del Proyecto

### 📁 Estructura de Archivos

```
ProyectoBCV/
├── 📄 bcv_scraper.py              # ✅ Script principal (Funcional)
├── 📄 config.py                  # ⚙️ Configuración centralizada
├── 📄 notifications.py           # 📧 Sistema de notificaciones
├── 📄 config_ejemplo.py          # 📋 Ejemplo de configuración
├── 📄 utils.py                   # 🔧 Utilidades reutilizables
├── 📄 requirements.txt           # 📦 Dependencias
├── 📄 ejecutar.bat              # 🚀 Script de ejecución (Windows)
├── 📄 configurar_tarea.bat      # ⏰ Configuración de tarea programada
├── 📄 subir_a_github.bat        # 📤 Script para subir a GitHub
├── 📄 precio_dolar_bcv.json     # 💾 Datos extraídos
├── 📄 bcv_scraper.log           # 📝 Log de operaciones
└── 📄 README.md                 # 📖 Esta documentación
```

### 🎯 Versión Actual

**`bcv_scraper.py`** - Script principal con paradigma funcional
- ✅ **Simple y directo**: Código limpio y fácil de entender
- ✅ **Funciones puras**: Sin efectos secundarios, fáciles de testear
- ✅ **Inmutabilidad**: Previene bugs y facilita debugging
- ✅ **Composición**: Funciones pequeñas que se combinan

## 🚀 Instalación y Uso

### Método 1: Ejecución Automática (Recomendado)

```bash
# Windows
ejecutar.bat

# Linux/Mac
python bcv_scraper.py
```

### Método 2: Instalación Manual

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar script
python bcv_scraper.py
```

### Método 3: Configuración de Tarea Programada

```bash
# Windows - Configurar tarea diaria
configurar_tarea.bat
```

## 📊 Estructura de Datos

### JSON de Salida

```json
[
  {
    "fecha_extraccion": "2025-10-22 20:51:57",
    "fecha_precio": "2025-10-23 00:00:00",
    "precio_dolar": 212.4837,
    "timestamp_extraccion": "2025-10-22T20:51:57.731987-04:00",
    "timestamp_precio": "2025-10-23T00:00:00",
    "zona_horaria": "America/Caracas (UTC-4)",
    "nota": "Precio corresponde al día indicado en fecha_precio"
  }
]
```

### 🕐 Lógica de Fechas

El BCV actualiza el precio a las **6:00 AM** pero ese precio corresponde al **día siguiente**:

- **Antes de las 6:00 AM**: El precio corresponde al día actual
- **Después de las 6:00 AM**: El precio corresponde al día siguiente

## 📧 Sistema de Notificaciones

### ✨ Características

- 📧 **Notificaciones por Email**: Recibe el precio por correo electrónico
- 📱 **Notificaciones por Telegram**: Recibe el precio por mensaje de Telegram
- 🔧 **Configuración Flexible**: Habilita/deshabilita cada tipo de notificación
- 🛡️ **Manejo de Errores**: Las notificaciones no afectan el proceso principal

### 📧 Configurar Email (Gmail)

1. **Habilita la verificación en 2 pasos** en tu cuenta de Google
2. **Genera una "Contraseña de aplicación"**:
   - Ve a: https://myaccount.google.com/security
   - Selecciona "Contraseñas de aplicaciones"
   - Genera una nueva contraseña para "Correo"
3. **Configura en `config.py`**:
   ```python
   EMAIL_ENABLED = True
   EMAIL_FROM = 'tu_email@gmail.com'
   EMAIL_PASSWORD = 'tu_contraseña_de_aplicacion'
   EMAIL_TO = 'destinatario@gmail.com'
   ```

### 📱 Configurar Telegram

1. **Crea un bot en Telegram**:
   - Busca @BotFather en Telegram
   - Envía `/newbot`
   - Sigue las instrucciones
   - Copia el token
2. **Obtén tu ID de chat**:
   - Busca @userinfobot en Telegram
   - Inicia conversación y te dará tu ID
3. **Configura en `config.py`**:
   ```python
   TELEGRAM_ENABLED = True
   TELEGRAM_BOT_TOKEN = '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz'
   TELEGRAM_CHAT_ID = '123456789'
   ```

### 🧪 Probar Notificaciones

```bash
# Probar el sistema de notificaciones
python notifications.py
```

## 🔧 Configuración Avanzada

### Variables de Configuración

```python
# config.py
BCV_URLS = [
    'https://www.bcv.org.ve/',
    'http://www.bcv.org.ve/',
    'https://bcv.org.ve/'
]

TIMEZONE = 'America/Caracas'
DATA_FILE = 'precio_dolar_bcv.json'
LOG_FILE = 'bcv_scraper.log'

# Notificaciones
NOTIFICATIONS_ENABLED = True
EMAIL_ENABLED = True
TELEGRAM_ENABLED = True
```

### Estrategias de Búsqueda

El script utiliza múltiples estrategias para encontrar el precio:

1. **Div específico** con `id='dolar'`
2. **Texto con palabras clave** USD/Dólar
3. **Tablas HTML** con datos de cambio
4. **Selectores CSS** específicos

## 🏛️ Paradigma de Programación

### 🧮 Paradigma Funcional

El proyecto utiliza **paradigma funcional** para mantener el código simple, directo y fácil de mantener:

```python
# Funciones puras sin efectos secundarios
def extract_and_save_price() -> bool:
    soup = fetch_page_content()      # 1. Obtener HTML
    price = find_dollar_price(soup)  # 2. Extraer precio
    return save_dollar_price(price)  # 3. Guardar datos
```

**Ventajas del Paradigma Funcional:**
- ✅ **Código simple y directo**: Fácil de entender y mantener
- ✅ **Funciones puras**: Sin efectos secundarios, fáciles de testear
- ✅ **Inmutabilidad**: Previene bugs y facilita debugging
- ✅ **Composición**: Funciones pequeñas que se combinan
- ✅ **Bajo acoplamiento**: Fácil de modificar y extender

## 📈 Programación Automática

### Windows (Task Scheduler)

1. Abrir "Programador de tareas"
2. Crear tarea básica:
   - **Nombre**: "BCV Dólar Scraper"
   - **Frecuencia**: Diaria
   - **Hora**: 18:00 (6 PM)
   - **Programa**: `python`
   - **Argumentos**: `bcv_scraper.py`

### Linux/Mac (Cron)

```bash
# Editar crontab
crontab -e

# Agregar línea para ejecutar diariamente a las 6 PM
0 18 * * * /usr/bin/python3 /ruta/completa/bcv_scraper.py
```

## 🌐 GitHub Actions (Opcional)

Para ejecución en la nube:

```yaml
# .github/workflows/bcv-scraper.yml
name: BCV Dólar Scraper
on:
  schedule:
    - cron: '0 22 * * *'  # 6 PM Venezuela (UTC-4)
  workflow_dispatch:
```

## 🛠️ Solución de Problemas

### Error de Conexión
- ✅ Verificar conexión a internet
- ✅ El sitio del BCV puede estar temporalmente fuera de servicio
- ✅ Revisar logs en `bcv_scraper.log`

### Error de Dependencias
```bash
pip install -r requirements.txt
```

### Precio No Encontrado
- ✅ El script incluye múltiples métodos de búsqueda
- ✅ Revisar logs para detalles específicos
- ✅ Verificar cambios en la estructura del sitio BCV

## 📊 Monitoreo y Análisis

### Logs Disponibles
- **`bcv_scraper.log`**: Registro detallado de operaciones
- **Consola**: Salida en tiempo real durante ejecución

### Análisis de Datos
Los datos se almacenan en `precio_dolar_bcv.json` y permiten:
- 📈 Análisis de tendencias del dólar
- 📅 Seguimiento histórico de precios
- 🔍 Identificación de patrones temporales

## 🔄 Extensibilidad

### Agregar Nuevas Fuentes
```python
# En config.py
BCV_URLS = [
    'https://www.bcv.org.ve/',
    'https://nueva-fuente.com/',  # Nueva fuente
]
```

### Nuevas Estrategias de Búsqueda
```python
def nueva_estrategia(soup: BeautifulSoup) -> Optional[str]:
    # Implementar nueva lógica de búsqueda
    pass

# Agregar a la lista de estrategias
search_strategies.append(nueva_estrategia)
```

## 📝 Changelog

### v3.0.0 - Sistema de Notificaciones
- ✅ **Notificaciones por Email**: Soporte completo para Gmail con autenticación segura
- ✅ **Notificaciones por Telegram**: Integración con bots de Telegram
- ✅ **Configuración Centralizada**: Gestión unificada de parámetros
- ✅ **Manejo de Errores Robusto**: Las notificaciones no afectan el proceso principal
- ✅ **Documentación Completa**: Guías paso a paso para configuración

### v2.0.0 - Lógica de Fechas Mejorada
- ✅ Distinción entre fecha de extracción y fecha del precio
- ✅ Lógica correcta para precios del BCV (actualización 6 AM)
- ✅ Estructura JSON mejorada con timestamps precisos

### v1.0.0 - Versión Inicial
- ✅ Extracción básica del precio del dólar
- ✅ Múltiples paradigmas de programación
- ✅ Scripts de automatización

## 🤝 Contribuciones

Para contribuir al proyecto:
1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios
4. Crear Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

**¡Monitorea el precio del dólar BCV de forma automática y confiable! 🇻🇪**