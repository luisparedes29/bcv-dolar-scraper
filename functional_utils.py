"""
Utilidades funcionales para el scraper del BCV
Aplicando paradigma funcional: funciones puras y composición
"""

import re
import logging
from typing import Optional, List, Callable, Any
from datetime import datetime
import pytz
from functools import partial, reduce


# Constantes
PRICE_PATTERN = re.compile(r'[\d,]+\.?\d*')
USD_KEYWORDS = ['USD', 'Dólar', 'Dollar']
TIMEZONE = 'America/Caracas'


# Funciones puras para manejo de texto
def clean_text(text: str) -> str:
    """Limpia texto eliminando espacios extra"""
    return text.strip() if text else ""


def contains_any_keyword(text: str, keywords: List[str]) -> bool:
    """Verifica si un texto contiene alguna palabra clave"""
    if not text or not keywords:
        return False
    text_upper = text.upper()
    return any(keyword.upper() in text_upper for keyword in keywords)


def extract_price_from_text(text: str) -> Optional[str]:
    """Extrae un precio de un texto usando regex"""
    if not text:
        return None
    match = PRICE_PATTERN.search(clean_text(text))
    return match.group() if match else None


def parse_price_to_float(price_text: str) -> Optional[float]:
    """Convierte texto de precio a número flotante"""
    if not price_text:
        return None
    try:
        clean_price = price_text.replace(',', '.')
        return float(clean_price)
    except ValueError:
        logging.error(f"No se pudo convertir el precio a número: {price_text}")
        return None


# Funciones puras para manejo de fechas
def get_venezuela_time() -> datetime:
    """Obtiene la hora actual de Venezuela"""
    venezuela_tz = pytz.timezone(TIMEZONE)
    return datetime.now(venezuela_tz)


def format_timestamp(dt: datetime) -> str:
    """Formatea un datetime a string legible"""
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def get_iso_timestamp(dt: datetime) -> str:
    """Obtiene timestamp en formato ISO"""
    return dt.isoformat()


# Funciones de composición
def compose(*functions):
    """Composición de funciones de derecha a izquierda"""
    def composed(x):
        return reduce(lambda acc, f: f(acc), reversed(functions), x)
    return composed


def pipe(*functions):
    """Composición de funciones de izquierda a derecha (pipe)"""
    def piped(x):
        return reduce(lambda acc, f: f(acc), functions, x)
    return piped


# Funciones de transformación
def transform_text(func: Callable[[str], str]) -> Callable[[str], str]:
    """Aplica una transformación a un texto"""
    return lambda text: func(clean_text(text))


def safe_parse_price() -> Callable[[str], Optional[float]]:
    """Crea una función segura para parsear precios"""
    return compose(
        lambda x: parse_price_to_float(x) if x else None,
        extract_price_from_text
    )


# Funciones de validación
def is_valid_price(price: Optional[float]) -> bool:
    """Valida si un precio es válido"""
    return price is not None and price > 0


def is_valid_text(text: str) -> bool:
    """Valida si un texto es válido para búsqueda"""
    return bool(text and clean_text(text))


# Funciones de logging funcional
def log_with_context(context: str) -> Callable[[str], None]:
    """Crea una función de logging con contexto"""
    return lambda message: logging.info(f"[{context}] {message}")


def log_error_with_context(context: str) -> Callable[[Exception], None]:
    """Crea una función de logging de errores con contexto"""
    return lambda error: logging.error(f"[{context}] {str(error)}")


# Funciones de transformación de datos
def create_price_entry(price: float) -> dict:
    """Crea una entrada de datos con timestamp"""
    now_venezuela = get_venezuela_time()
    return {
        'fecha': format_timestamp(now_venezuela),
        'precio_dolar': price,
        'timestamp': get_iso_timestamp(now_venezuela),
        'zona_horaria': f'{TIMEZONE} (UTC-4)'
    }


def append_to_list(item: Any) -> Callable[[List[Any]], List[Any]]:
    """Crea una función que agrega un elemento a una lista (inmutable)"""
    return lambda lst: lst + [item]


# Funciones de búsqueda funcional
def search_with_strategy(strategy: Callable) -> Callable:
    """Crea una función de búsqueda con una estrategia específica"""
    def search_function(soup):
        try:
            return strategy(soup)
        except Exception as e:
            logging.warning(f"Error en estrategia de búsqueda: {e}")
            return None
    return search_function


def try_strategies(*strategies) -> Callable:
    """Crea una función que prueba múltiples estrategias"""
    def try_all(soup):
        for strategy in strategies:
            result = search_with_strategy(strategy)(soup)
            if result:
                return result
        return None
    return try_all


# Funciones de validación de datos
def validate_price_data(data: dict) -> bool:
    """Valida que los datos de precio sean correctos"""
    required_fields = ['fecha', 'precio_dolar', 'timestamp']
    return all(field in data for field in required_fields)


def filter_valid_prices(prices: List[dict]) -> List[dict]:
    """Filtra precios válidos de una lista"""
    return [price for price in prices if validate_price_data(price)]


# Funciones de utilidad para logging
def log_success(message: str) -> None:
    """Log de éxito"""
    logging.info(f"✅ {message}")


def log_error(message: str) -> None:
    """Log de error"""
    logging.error(f"❌ {message}")


def log_warning(message: str) -> None:
    """Log de advertencia"""
    logging.warning(f"⚠️ {message}")


# Funciones de transformación de listas
def map_prices(func: Callable) -> Callable[[List[dict]], List[dict]]:
    """Aplica una función a cada precio en una lista"""
    return lambda prices: [func(price) for price in prices]


def filter_prices(predicate: Callable) -> Callable[[List[dict]], List[dict]]:
    """Filtra precios basado en un predicado"""
    return lambda prices: [price for price in prices if predicate(price)]


# Funciones de reducción
def sum_prices(prices: List[dict]) -> float:
    """Suma todos los precios de una lista"""
    return sum(price.get('precio_dolar', 0) for price in prices)


def average_price(prices: List[dict]) -> float:
    """Calcula el precio promedio"""
    if not prices:
        return 0.0
    return sum_prices(prices) / len(prices)


# Funciones de ordenamiento
def sort_by_date(prices: List[dict]) -> List[dict]:
    """Ordena precios por fecha"""
    return sorted(prices, key=lambda x: x.get('timestamp', ''))


def sort_by_price(prices: List[dict]) -> List[dict]:
    """Ordena precios por valor"""
    return sorted(prices, key=lambda x: x.get('precio_dolar', 0))


# Funciones de búsqueda en listas
def find_latest_price(prices: List[dict]) -> Optional[dict]:
    """Encuentra el precio más reciente"""
    if not prices:
        return None
    return max(prices, key=lambda x: x.get('timestamp', ''))


def find_price_by_date(prices: List[dict], target_date: str) -> Optional[dict]:
    """Encuentra un precio por fecha específica"""
    return next((price for price in prices if price.get('fecha', '').startswith(target_date)), None)
