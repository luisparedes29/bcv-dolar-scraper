"""
Configuración centralizada para el scraper del BCV
Aplicando principios de Clean Code: configuración separada y clara
"""

from typing import List, Dict, Any
import os


class ScraperConfig:
    """Configuración principal del scraper"""
    
    # URLs del BCV
    BCV_URLS = [
        'https://www.bcv.org.ve/',
        'http://www.bcv.org.ve/',
        'https://bcv.org.ve/'
    ]
    
    # Headers HTTP
    HTTP_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Configuración de archivos
    DATA_FILE = 'precio_dolar_bcv.json'
    LOG_FILE = 'bcv_scraper.log'
    
    # Configuración de red
    REQUEST_TIMEOUT = 60
    MAX_RETRIES = 3
    
    # Configuración de zona horaria
    TIMEZONE = 'America/Caracas'
    
    # Configuración de logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    
    # Selectores CSS para búsqueda de precios
    PRICE_SELECTORS = [
        '.dolar', '.usd', '.price', '.valor', '.tipo-cambio',
        '[class*="dolar"]', '[class*="usd"]', '[class*="price"]'
    ]
    
    # Palabras clave para búsqueda de USD
    USD_KEYWORDS = ['USD', 'Dólar', 'Dollar']
    
    # Patrón regex para extraer precios
    PRICE_PATTERN = r'[\d,]+\.?\d*'
    
    @classmethod
    def get_data_file_path(cls) -> str:
        """Obtiene la ruta completa del archivo de datos"""
        return os.path.abspath(cls.DATA_FILE)
    
    @classmethod
    def get_log_file_path(cls) -> str:
        """Obtiene la ruta completa del archivo de log"""
        return os.path.abspath(cls.LOG_FILE)
