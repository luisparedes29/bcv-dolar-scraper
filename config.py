"""
Configuración centralizada para el scraper del BCV
Aplicando principios de Clean Code: configuración separada y clara
"""

from typing import List, Dict, Any
import os

# Intentar cargar configuración local si existe
try:
    from configurar_env import configurar_variables
    configurar_variables()
    print("✅ Variables de entorno cargadas desde configurar_env.py")
except ImportError:
    print("⚠️  configurar_env.py no encontrado - usando variables de entorno del sistema")


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
    
    # Configuración de notificaciones
    NOTIFICATIONS_ENABLED = True
    
    # Configuración de email (desde variables de entorno)
    EMAIL_ENABLED = True
    EMAIL_SMTP_SERVER = 'smtp.gmail.com'
    EMAIL_SMTP_PORT = 587
    EMAIL_FROM = os.getenv('EMAIL_FROM', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    EMAIL_TO = os.getenv('EMAIL_TO', '')
    EMAIL_SUBJECT = 'Precio del Dólar BCV - Actualización'
    
    # Configuración de Telegram (desde variables de entorno)
    TELEGRAM_ENABLED = True
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    
    @classmethod
    def get_data_file_path(cls) -> str:
        """Obtiene la ruta completa del archivo de datos"""
        return os.path.abspath(cls.DATA_FILE)
    
    @classmethod
    def get_log_file_path(cls) -> str:
        """Obtiene la ruta completa del archivo de log"""
        return os.path.abspath(cls.LOG_FILE)
    
    @classmethod
    def is_email_configured(cls) -> bool:
        """Verifica si la configuración de email está completa"""
        return all([
            cls.EMAIL_FROM,
            cls.EMAIL_PASSWORD,
            cls.EMAIL_TO
        ])
    
    @classmethod
    def is_telegram_configured(cls) -> bool:
        """Verifica si la configuración de Telegram está completa"""
        return all([
            cls.TELEGRAM_BOT_TOKEN,
            cls.TELEGRAM_CHAT_ID
        ])
