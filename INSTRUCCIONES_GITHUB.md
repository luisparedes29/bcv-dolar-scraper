# 🚀 Instrucciones para Configurar GitHub Actions

## 📋 Pasos para Configurar el Scraper Automático

### 1. Crear Repositorio en GitHub

1. **Ve a [GitHub.com](https://github.com)** y haz login
2. **Haz clic en "New repository"** (botón verde)
3. **Configura el repositorio:**
   - **Nombre**: `bcv-dolar-scraper`
   - **Descripción**: "Extractor automático del precio del dólar del BCV"
   - **Visibilidad**: ✅ **Público** (importante para GitHub Actions gratis)
   - **NO marques** "Add a README file"
   - **NO marques** "Add .gitignore"
   - **NO marques** "Choose a license"
4. **Haz clic en "Create repository"**

### 2. Subir el Código

#### Opción A: Usar el Script Automático (Recomendado)
1. **Ejecuta** `subir_a_github.bat` (doble clic)
2. **Sigue las instrucciones** en pantalla
3. **Pega la URL** del repositorio cuando se solicite

#### Opción B: Comandos Manuales
```bash
# Conectar con GitHub (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/bcv-dolar-scraper.git

# Subir código
git push -u origin main
```

### 3. Activar GitHub Actions

1. **Ve a la pestaña "Actions"** en tu repositorio
2. **GitHub Actions se activará automáticamente**
3. **Verás el workflow "BCV Dólar Scraper"**

### 4. Probar la Ejecución

1. **Ve a Actions → BCV Dólar Scraper**
2. **Haz clic en "Run workflow"**
3. **Selecciona "main" y haz clic en "Run workflow"**
4. **Espera a que termine** (2-3 minutos)

### 5. Verificar los Resultados

1. **Ve a la pestaña "Code"** en tu repositorio
2. **Verifica que existe** `precio_dolar_bcv.json`
3. **Haz clic en el archivo** para ver el contenido
4. **Deberías ver** el precio del dólar extraído

## ⏰ Programación Automática

- **Frecuencia**: Diaria
- **Hora**: 6:00 PM (hora de Venezuela)
- **Zona Horaria**: UTC-4
- **Cron**: `0 22 * * *` (22:00 UTC = 18:00 Venezuela)

## 📊 Monitoreo

### Ver Ejecuciones
- **Actions Tab** → Ver historial de ejecuciones
- **Commits** → Ver commits automáticos con nuevos datos

### Ver Datos
- **Archivo JSON** → Historial completo de precios
- **Logs** → Detalles de cada ejecución

## 🔧 Configuración Avanzada

### Cambiar Hora de Ejecución
Edita `.github/workflows/bcv-scraper.yml`:
```yaml
schedule:
  - cron: '0 22 * * *'  # Cambia el primer número (0-59 minutos)
```

### Ejecutar Manualmente
1. **Actions** → **BCV Dólar Scraper**
2. **Run workflow** → **Run workflow**

## 🆘 Solución de Problemas

### Error: "Workflow not found"
- Verifica que el archivo `.github/workflows/bcv-scraper.yml` existe
- Asegúrate de que el repositorio es público

### Error: "Permission denied"
- Verifica que el repositorio es público
- Revisa que tienes permisos de escritura

### Error: "No data found"
- Revisa los logs en la pestaña Actions
- Verifica que el sitio del BCV esté accesible

## 📈 Beneficios de GitHub Actions

✅ **Gratis** para repositorios públicos
✅ **No requiere computadora encendida**
✅ **Ejecución automática diaria**
✅ **Almacenamiento en la nube**
✅ **Historial completo de datos**
✅ **Logs detallados**
✅ **Ejecución manual disponible**

## 🎯 Resultado Final

Después de la configuración tendrás:
- **Ejecución automática** diaria a las 6 PM
- **Archivo JSON** con historial de precios
- **Logs detallados** de cada ejecución
- **Acceso desde cualquier lugar** a los datos
- **Sin dependencias** de tu computadora local

---

**¡Disfruta del monitoreo automático del precio del dólar! 🇻🇪**
