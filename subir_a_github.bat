@echo off
echo ========================================
echo    SUBIR PROYECTO A GITHUB
echo ========================================
echo.
echo Este script te ayudará a subir el proyecto a GitHub
echo.
echo PASOS A SEGUIR:
echo.
echo 1. Ve a https://github.com y crea un nuevo repositorio
echo    - Nombre: bcv-dolar-scraper
echo    - Hazlo PUBLICO (para GitHub Actions gratis)
echo    - NO inicialices con README
echo.
echo 2. Copia la URL del repositorio (algo como: https://github.com/TU_USUARIO/bcv-dolar-scraper.git)
echo.
echo 3. Presiona cualquier tecla cuando hayas creado el repositorio...
pause
echo.
echo 4. Ahora pega la URL del repositorio y presiona Enter:
set /p REPO_URL="URL del repositorio: "
echo.
echo Conectando con GitHub...
git remote add origin %REPO_URL%
echo.
echo Subiendo código a GitHub...
git push -u origin main
echo.
echo ¡Listo! Tu proyecto está en GitHub.
echo.
echo PRÓXIMOS PASOS:
echo 1. Ve a la pestaña "Actions" en tu repositorio
echo 2. GitHub Actions se activará automáticamente
echo 3. El scraper se ejecutará diariamente a las 6 PM
echo.
echo Presiona cualquier tecla para salir...
pause
