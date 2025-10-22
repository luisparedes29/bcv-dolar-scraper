# 🇻🇪 BCV Dólar Scraper - GitHub Actions

Este proyecto automatiza la extracción diaria del precio del dólar desde el sitio web del Banco Central de Venezuela (BCV) usando GitHub Actions.

## 🚀 Características

- ✅ **Ejecución Automática**: Se ejecuta diariamente a las 6 PM (hora de Venezuela)
- ✅ **Sin Dependencias Locales**: No requiere que tu computadora esté encendida
- ✅ **Almacenamiento en GitHub**: Los datos se guardan directamente en el repositorio
- ✅ **Historial Completo**: Mantiene un registro de todos los precios extraídos
- ✅ **Logs Detallados**: Registro completo de todas las operaciones

## 📊 Datos Extraídos

El script extrae y almacena:
- **Precio del dólar** en Bolívares Soberanos (Bs)
- **Fecha y hora** de la extracción
- **Timestamp** para análisis temporal

## 📁 Archivos del Proyecto

- `bcv_scraper.py` - Script principal de extracción
- `requirements.txt` - Dependencias de Python
- `.github/workflows/bcv-scraper.yml` - Configuración de GitHub Actions
- `precio_dolar_bcv.json` - Archivo con el historial de precios
- `bcv_scraper.log` - Log de operaciones

## 🔧 Configuración

### 1. Crear Repositorio en GitHub

1. Ve a [GitHub](https://github.com) y crea un nuevo repositorio
2. Nombra el repositorio: `bcv-dolar-scraper`
3. Hazlo **público** para usar GitHub Actions gratis

### 2. Subir el Código

```bash
# Inicializar git (si no está inicializado)
git init

# Agregar archivos
git add .

# Primer commit
git commit -m "Configuración inicial del BCV Scraper"

# Conectar con GitHub
git remote add origin https://github.com/TU_USUARIO/bcv-dolar-scraper.git

# Subir código
git push -u origin main
```

### 3. Activar GitHub Actions

1. Ve a la pestaña **"Actions"** en tu repositorio
2. GitHub Actions se activará automáticamente
3. El workflow se ejecutará diariamente a las 6 PM

## 📅 Programación

- **Frecuencia**: Diaria
- **Hora**: 6:00 PM (hora de Venezuela)
- **Zona Horaria**: UTC-4 (Venezuela)

## 📈 Monitoreo

Puedes monitorear las ejecuciones en:
- **Actions Tab**: Ver el estado de las ejecuciones
- **Commits**: Ver los commits automáticos con nuevos datos
- **Archivo JSON**: Ver el historial completo de precios

## 🔍 Estructura del JSON

```json
[
  {
    "fecha": "2024-01-15 18:00:00",
    "precio_dolar": 210.2825,
    "timestamp": "2024-01-15T18:00:00.123456"
  }
]
```

## 🛠️ Ejecución Manual

Puedes ejecutar el workflow manualmente:
1. Ve a **Actions** → **BCV Dólar Scraper**
2. Haz clic en **"Run workflow"**
3. Selecciona la rama y haz clic en **"Run workflow"**

## 📊 Análisis de Datos

Los datos se almacenan en `precio_dolar_bcv.json` y puedes:
- Descargar el archivo para análisis local
- Usar APIs de GitHub para acceder a los datos
- Crear visualizaciones con los datos históricos

## 🆘 Solución de Problemas

### Error de conexión
- Verifica que el sitio del BCV esté accesible
- Revisa los logs en la pestaña "Actions"

### Error de dependencias
- El workflow instala automáticamente las dependencias
- Si hay problemas, revisa el archivo `requirements.txt`

## 📞 Soporte

Para reportar problemas:
1. Ve a la pestaña **"Issues"** en GitHub
2. Crea un nuevo issue con la descripción del problema
3. Incluye los logs de la ejecución fallida

---

**¡Disfruta del monitoreo automático del precio del dólar! 🇻🇪**
