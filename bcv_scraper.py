#!/usr/bin/env python3
"""
Script para extraer el precio del dólar del BCV (Banco Central de Venezuela)
Aplicando paradigma funcional:

✅ Funciones puras (sin efectos secundarios)
✅ Composición de funciones
✅ Inmutabilidad de datos
✅ Sin estado mutable
✅ Código más simple y directo
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import logging
import re
import urllib3
from datetime import datetime
import pytz
from typing import Optional, List, Dict, Any, Tuple
from functools import partial
from config import ScraperConfig

# Configuración desde el módulo centralizado
BCV_URLS = ScraperConfig.BCV_URLS
HTTP_HEADERS = ScraperConfig.HTTP_HEADERS
DATA_FILE = ScraperConfig.DATA_FILE
LOG_FILE = ScraperConfig.LOG_FILE
REQUEST_TIMEOUT = ScraperConfig.REQUEST_TIMEOUT
TIMEZONE = ScraperConfig.TIMEZONE
USD_KEYWORDS = ScraperConfig.USD_KEYWORDS
PRICE_PATTERN = re.compile(ScraperConfig.PRICE_PATTERN)

# Deshabilitar advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def setup_logging() -> None:
    """Configura el sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )


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


def make_http_request(url: str) -> Optional[requests.Response]:
    """Realiza una petición HTTP"""
    try:
        logging.info(f"Accediendo a {url}")
        response = requests.get(
            url,
            headers=HTTP_HEADERS,
            timeout=REQUEST_TIMEOUT,
            verify=False
        )
        response.raise_for_status()
        return response
    except Exception as e:
        logging.warning(f"Error con {url}: {e}")
        return None


def fetch_page_content() -> Optional[BeautifulSoup]:
    """Obtiene el contenido HTML de la página del BCV"""
    for url in BCV_URLS:
        response = make_http_request(url)
        if response:
            return BeautifulSoup(response.content, 'html.parser')
    
    logging.error("No se pudo acceder a ninguna URL del BCV")
    return None


def search_in_dollar_div(soup: BeautifulSoup) -> Optional[str]:
    """Busca precio en el div específico con id='dolar'"""
    dolar_div = soup.find('div', id='dolar')
    if not dolar_div:
        return None
    
    strong_element = dolar_div.find('strong')
    if not strong_element:
        return None
    
    price_text = clean_text(strong_element.get_text())
    return extract_price_from_text(price_text)


def search_in_usd_text(soup: BeautifulSoup) -> Optional[str]:
    """Busca precio en texto que contenga palabras clave de USD"""
    for keyword in USD_KEYWORDS:
        elements = soup.find_all(string=lambda text: keyword.lower() in text.lower() if text else False)
        for element in elements:
            if element.parent:
                price_text = clean_text(element.parent.get_text())
                price = extract_price_from_text(price_text)
                if price:
                    return price
    return None


def search_in_tables(soup: BeautifulSoup) -> Optional[str]:
    """Busca precio en tablas HTML"""
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            for cell in cells:
                cell_text = clean_text(cell.get_text())
                if contains_any_keyword(cell_text, USD_KEYWORDS):
                    price = extract_price_from_text(cell_text)
                    if price:
                        return price
    return None


def search_with_css_selectors(soup: BeautifulSoup) -> Optional[str]:
    """Busca precio usando selectores CSS específicos"""
    selectors = ScraperConfig.PRICE_SELECTORS
    
    for selector in selectors:
        elements = soup.select(selector)
        for element in elements:
            text = clean_text(element.get_text())
            price = extract_price_from_text(text)
            if price:
                return price
    return None


def find_dollar_price(soup: BeautifulSoup) -> Optional[float]:
    """Busca el precio del dólar usando múltiples estrategias"""
    if not soup:
        return None
    
    # Estrategias de búsqueda en orden de prioridad
    search_strategies = [
        search_in_dollar_div,
        search_in_usd_text,
        search_in_tables,
        search_with_css_selectors
    ]
    
    for strategy in search_strategies:
        try:
            price_text = strategy(soup)
            if price_text:
                price_float = parse_price_to_float(price_text)
                if price_float:
                    logging.info(f"Precio encontrado: {price_text}")
                    return price_float
        except Exception as e:
            logging.warning(f"Error en estrategia de búsqueda: {e}")
            continue
    
    logging.warning("No se encontró el precio del dólar en la página")
    return None


def calculate_price_date(extraction_time: datetime) -> datetime:
    """
    Calcula la fecha a la que corresponde el precio del dólar.
    
    El precio se actualiza a las 6:00 AM pero corresponde al día siguiente.
    Si se extrae antes de las 6:00 AM, el precio corresponde al día actual.
    Si se extrae después de las 6:00 AM, el precio corresponde al día siguiente.
    """
    # Si es antes de las 6:00 AM, el precio corresponde al día actual
    if extraction_time.hour < 6:
        return extraction_time.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        # Si es después de las 6:00 AM, el precio corresponde al día siguiente
        from datetime import timedelta
        next_day = extraction_time + timedelta(days=1)
        return next_day.replace(hour=0, minute=0, second=0, microsecond=0)


def create_price_entry(price: float) -> Dict[str, Any]:
    """Crea una entrada de datos con timestamp y fecha del precio"""
    now_venezuela = get_venezuela_time()
    price_date = calculate_price_date(now_venezuela)
    
    return {
        'fecha_extraccion': format_timestamp(now_venezuela),
        'fecha_precio': format_timestamp(price_date),
        'precio_dolar': price,
        'timestamp_extraccion': get_iso_timestamp(now_venezuela),
        'timestamp_precio': get_iso_timestamp(price_date),
        'zona_horaria': f'{TIMEZONE} (UTC-4)',
        'nota': 'Precio corresponde al día indicado en fecha_precio'
    }


def load_existing_data() -> List[Dict[str, Any]]:
    """Carga datos existentes del archivo JSON"""
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logging.warning(f"Error al cargar datos existentes: {e}")
        return []


def save_price_to_file(data: List[Dict[str, Any]]) -> bool:
    """Escribe datos al archivo JSON"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        logging.error(f"Error al escribir archivo: {e}")
        return False


def save_dollar_price(price: float) -> bool:
    """Guarda el precio del dólar en el archivo JSON"""
    try:
        data_entry = create_price_entry(price)
        existing_data = load_existing_data()
        updated_data = existing_data + [data_entry]  # Inmutabilidad
        
        success = save_price_to_file(updated_data)
        if success:
            logging.info(f"Precio guardado: {price} Bs")
        return success
        
    except Exception as e:
        logging.error(f"Error al guardar el precio: {e}")
        return False


def extract_and_save_price() -> bool:
    """Función principal que extrae y guarda el precio del dólar"""
    logging.info("Iniciando extracción del precio del dólar del BCV")
    
    # Paso 1: Obtener contenido de la página
    soup = fetch_page_content()
    if not soup:
        logging.error("No se pudo obtener el contenido de la página")
        return False
    
    # Paso 2: Extraer precio del dólar
    price = find_dollar_price(soup)
    if price is None:
        logging.error("No se pudo obtener el precio del dólar")
        return False
    
    # Paso 3: Guardar precio
    success = save_dollar_price(price)
    if not success:
        logging.error("Error al guardar el precio")
        return False
    
    logging.info("Proceso completado exitosamente")
    return True


def main():
    """Función principal del script"""
    setup_logging()
    
    success = extract_and_save_price()
    
    if success:
        print("Precio del dólar extraído y guardado exitosamente")
    else:
        print("Error al extraer el precio del dólar")
        exit(1)


if __name__ == "__main__":
    main()
