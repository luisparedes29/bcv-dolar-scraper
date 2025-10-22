@echo off
echo ========================================
echo    SCRIPTER BCV - EXTRACTOR DE PRECIOS
echo ========================================
echo.
echo Instalando dependencias...
pip install -r requirements.txt
echo.
echo Ejecutando script de extracción del precio del dólar...
python bcv_scraper.py
echo.
echo Presiona cualquier tecla para salir...
pause
