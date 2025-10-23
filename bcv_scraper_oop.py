#!/usr/bin/env python3
"""
Script para extraer el precio del dólar del BCV (Banco Central de Venezuela)
Aplicando principios de Clean Code:

✅ Funciones pequeñas con una sola responsabilidad
✅ Nombres descriptivos y claros
✅ Eliminación de código duplicado
✅ Separación de responsabilidades
✅ Configuración centralizada
✅ Manejo de errores robusto
✅ Documentación clara
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import logging
import urllib3
from typing import Optional, List, Dict, Any

from config import ScraperConfig
from utils import PriceParser, DateTimeUtils, TextUtils, LogUtils


class WebClient:
    """Cliente HTTP para hacer peticiones al BCV"""
    
    def __init__(self):
        self.config = ScraperConfig()
        self._disable_ssl_warnings()
    
    def _disable_ssl_warnings(self) -> None:
        """Deshabilita advertencias SSL"""
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def fetch_page_content(self) -> Optional[BeautifulSoup]:
        """
        Obtiene el contenido HTML de la página del BCV
        
        Returns:
            BeautifulSoup object o None si falla
        """
        for url in self.config.BCV_URLS:
            try:
                response = self._make_request(url)
                if response:
                    return BeautifulSoup(response.content, 'html.parser')
            except Exception as e:
                LogUtils.log_error_with_context(e, f"acceso a {url}")
                continue
        
        logging.error("No se pudo acceder a ninguna URL del BCV")
        return None
    
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """Realiza una petición HTTP"""
        try:
            logging.info(f"Accediendo a {url}")
            response = requests.get(
                url,
                headers=self.config.HTTP_HEADERS,
                timeout=self.config.REQUEST_TIMEOUT,
                verify=False
            )
            response.raise_for_status()
            return response
        except Exception as e:
            LogUtils.log_error_with_context(e, f"petición a {url}")
            return None


class DollarPriceFinder:
    """Encuentra el precio del dólar en el HTML"""
    
    def __init__(self):
        self.config = ScraperConfig()
        self.price_parser = PriceParser()
    
    def find_dollar_price(self, soup: BeautifulSoup) -> Optional[float]:
        """
        Busca el precio del dólar usando múltiples estrategias
        
        Args:
            soup: BeautifulSoup object con el HTML
            
        Returns:
            Precio como float o None si no se encuentra
        """
        if not soup:
            return None
        
        # Estrategias de búsqueda en orden de prioridad
        search_strategies = [
            self._search_in_dollar_div,
            self._search_in_usd_text,
            self._search_in_tables,
            self._search_with_css_selectors
        ]
        
        for strategy in search_strategies:
            try:
                price_text = strategy(soup)
                if price_text:
                    price_float = self.price_parser.parse_price_to_float(price_text)
                    if price_float:
                        LogUtils.log_success_with_data("Precio encontrado", price_text)
                        return price_float
            except Exception as e:
                LogUtils.log_error_with_context(e, f"estrategia de búsqueda")
                continue
        
        logging.warning("No se encontró el precio del dólar en la página")
        return None
    
    def _search_in_dollar_div(self, soup: BeautifulSoup) -> Optional[str]:
        """Busca en el div específico con id='dolar'"""
        dolar_div = soup.find('div', id='dolar')
        if not dolar_div:
            return None
        
        strong_element = dolar_div.find('strong')
        if not strong_element:
            return None
        
        price_text = TextUtils.clean_text(strong_element.get_text())
        return self.price_parser.extract_price_from_text(price_text)
    
    def _search_in_usd_text(self, soup: BeautifulSoup) -> Optional[str]:
        """Busca en texto que contenga palabras clave de USD"""
        for keyword in self.config.USD_KEYWORDS:
            elements = soup.find_all(string=lambda text: keyword.lower() in text.lower() if text else False)
            for element in elements:
                if element.parent:
                    price_text = TextUtils.clean_text(element.parent.get_text())
                    price = self.price_parser.extract_price_from_text(price_text)
                    if price:
                        return price
        return None
    
    def _search_in_tables(self, soup: BeautifulSoup) -> Optional[str]:
        """Busca en tablas HTML"""
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                for cell in cells:
                    cell_text = TextUtils.clean_text(cell.get_text())
                    if TextUtils.contains_any_keyword(cell_text, self.config.USD_KEYWORDS):
                        price = self.price_parser.extract_price_from_text(cell_text)
                        if price:
                            return price
        return None
    
    def _search_with_css_selectors(self, soup: BeautifulSoup) -> Optional[str]:
        """Busca usando selectores CSS específicos"""
        for selector in self.config.PRICE_SELECTORS:
            elements = soup.select(selector)
            for element in elements:
                text = TextUtils.clean_text(element.get_text())
                price = self.price_parser.extract_price_from_text(text)
                if price:
                    return price
        return None


class DataStorage:
    """Maneja el almacenamiento de datos"""
    
    def __init__(self):
        self.config = ScraperConfig()
    
    def save_dollar_price(self, price: float) -> bool:
        """
        Guarda el precio del dólar en el archivo JSON
        
        Args:
            price: Precio del dólar a guardar
            
        Returns:
            True si se guardó exitosamente, False en caso contrario
        """
        try:
            data_entry = self._create_price_entry(price)
            existing_data = self._load_existing_data()
            existing_data.append(data_entry)
            
            self._write_data_to_file(existing_data)
            LogUtils.log_success_with_data("Precio guardado", f"{price} Bs")
            return True
            
        except Exception as e:
            LogUtils.log_error_with_context(e, "guardado de precio")
            return False
    
    def _create_price_entry(self, price: float) -> Dict[str, Any]:
        """Crea una entrada de datos con timestamp"""
        now_venezuela = DateTimeUtils.get_venezuela_time()
        return {
            'fecha': DateTimeUtils.format_timestamp(now_venezuela),
            'precio_dolar': price,
            'timestamp': DateTimeUtils.get_iso_timestamp(now_venezuela),
            'zona_horaria': f'{self.config.TIMEZONE} (UTC-4)'
        }
    
    def _load_existing_data(self) -> List[Dict[str, Any]]:
        """Carga datos existentes del archivo JSON"""
        if not os.path.exists(self.config.DATA_FILE):
            return []
        
        try:
            with open(self.config.DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            LogUtils.log_error_with_context(e, "carga de datos existentes")
            return []
    
    def _write_data_to_file(self, data: List[Dict[str, Any]]) -> None:
        """Escribe datos al archivo JSON"""
        with open(self.config.DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


class BCVDollarScraper:
    """Clase principal que coordina el proceso de extracción"""
    
    def __init__(self):
        self.web_client = WebClient()
        self.price_finder = DollarPriceFinder()
        self.data_storage = DataStorage()
    
    def run(self) -> bool:
        """
        Ejecuta el proceso completo de extracción y guardado
        
        Returns:
            True si el proceso fue exitoso, False en caso contrario
        """
        logging.info("Iniciando extracción del precio del dólar del BCV")
        
        # Paso 1: Obtener contenido de la página
        soup = self.web_client.fetch_page_content()
        if not soup:
            logging.error("No se pudo obtener el contenido de la página")
            return False
        
        # Paso 2: Extraer precio del dólar
        price = self.price_finder.find_dollar_price(soup)
        if price is None:
            logging.error("No se pudo obtener el precio del dólar")
            return False
        
        # Paso 3: Guardar precio
        success = self.data_storage.save_dollar_price(price)
        if not success:
            logging.error("Error al guardar el precio")
            return False
        
        logging.info("Proceso completado exitosamente")
        return True


def main():
    """Función principal del script"""
    # Configurar logging
    LogUtils.setup_logging(
        log_file=ScraperConfig.get_log_file_path(),
        log_level=ScraperConfig.LOG_LEVEL
    )
    
    # Ejecutar scraper
    scraper = BCVDollarScraper()
    success = scraper.run()
    
    # Mostrar resultado
    if success:
        print("Precio del dólar extraído y guardado exitosamente")
    else:
        print("Error al extraer el precio del dólar")
        exit(1)


if __name__ == "__main__":
    main()
