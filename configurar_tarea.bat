@echo off
echo ========================================
echo   CONFIGURADOR DE TAREA PROGRAMADA
echo ========================================
echo.
echo Este script configurará la tarea para ejecutar
echo el extractor de precios del BCV todos los días a las 6 PM
echo.
echo Presiona cualquier tecla para continuar...
pause

echo Creando tarea programada...
schtasks /create /tn "BCV Dolar Scraper" /tr "python \"%~dp0bcv_scraper.py\"" /sc daily /st 18:00 /f

if %errorlevel% equ 0 (
    echo.
    echo ✅ Tarea programada creada exitosamente!
    echo La tarea se ejecutará todos los días a las 6:00 PM
    echo.
    echo Para ver la tarea: schtasks /query /tn "BCV Dolar Scraper"
    echo Para eliminar la tarea: schtasks /delete /tn "BCV Dolar Scraper" /f
) else (
    echo.
    echo ❌ Error al crear la tarea programada
    echo Asegúrate de ejecutar como administrador
)

echo.
echo Presiona cualquier tecla para salir...
pause
