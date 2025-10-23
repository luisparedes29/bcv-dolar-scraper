"""
Utilidades para el scraper del BCV
Aplicando Clean Code: funciones puras y reutilizables
"""

import re
import logging
from typing import Optional, List
from datetime import datetime
import pytz


class PriceParser:
    """Utilidades para parsear precios"""
    
    PRICE_PATTERN = re.compile(r'[\d,]+\.?\d*')
    
    @classmethod
    def extract_price_from_text(cls, text: str) -> Optional[str]:
        """
        Extrae un precio de un texto usando regex
        
        Args:
            text: Texto que puede contener un precio
            
        Returns:
            String del precio encontrado o None
        """
        if not text:
            return None
            
        match = cls.PRICE_PATTERN.search(text.strip())
        return match.group() if match else None
    
    @classmethod
    def parse_price_to_float(cls, price_text: str) -> Optional[float]:
        """
        Convierte texto de precio a número flotante
        
        Args:
            price_text: Texto del precio (ej: "36,50" o "36.50")
            
        Returns:
            Precio como float o None si no se puede convertir
        """
        if not price_text:
            return None
            
        try:
            # Reemplazar coma por punto para formato decimal correcto
            clean_price = price_text.replace(',', '.')
            return float(clean_price)
        except ValueError:
            logging.error(f"No se pudo convertir el precio a número: {price_text}")
            return None


class DateTimeUtils:
    """Utilidades para manejo de fechas y horas"""
    
    @staticmethod
    def get_venezuela_time() -> datetime:
        """
        Obtiene la hora actual de Venezuela (UTC-4)
        
        Returns:
            datetime: Hora actual en zona horaria de Venezuela
        """
        venezuela_tz = pytz.timezone('America/Caracas')
        return datetime.now(venezuela_tz)
    
    @staticmethod
    def format_timestamp(dt: datetime) -> str:
        """
        Formatea un datetime a string legible
        
        Args:
            dt: datetime a formatear
            
        Returns:
            String formateado (YYYY-MM-DD HH:MM:SS)
        """
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def get_iso_timestamp(dt: datetime) -> str:
        """
        Obtiene timestamp en formato ISO
        
        Args:
            dt: datetime a convertir
            
        Returns:
            String en formato ISO
        """
        return dt.isoformat()


class TextUtils:
    """Utilidades para procesamiento de texto"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Limpia texto eliminando espacios extra y caracteres no deseados
        
        Args:
            text: Texto a limpiar
            
        Returns:
            Texto limpio
        """
        if not text:
            return ""
        return text.strip()
    
    @staticmethod
    def contains_any_keyword(text: str, keywords: List[str]) -> bool:
        """
        Verifica si un texto contiene alguna de las palabras clave
        
        Args:
            text: Texto a verificar
            keywords: Lista de palabras clave
            
        Returns:
            True si contiene alguna palabra clave
        """
        if not text or not keywords:
            return False
            
        text_upper = text.upper()
        return any(keyword.upper() in text_upper for keyword in keywords)


class LogUtils:
    """Utilidades para logging"""
    
    @staticmethod
    def setup_logging(log_file: str, log_level: str = 'INFO') -> None:
        """
        Configura el sistema de logging
        
        Args:
            log_file: Archivo donde guardar los logs
            log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
        """
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    @staticmethod
    def log_error_with_context(error: Exception, context: str) -> None:
        """
        Registra un error con contexto adicional
        
        Args:
            error: Excepción capturada
            context: Contexto donde ocurrió el error
        """
        logging.error(f"Error en {context}: {str(error)}")
    
    @staticmethod
    def log_success_with_data(message: str, data: any) -> None:
        """
        Registra un mensaje de éxito con datos
        
        Args:
            message: Mensaje de éxito
            data: Datos relacionados al éxito
        """
        logging.info(f"{message}: {data}")
