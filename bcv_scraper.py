#!/usr/bin/env python3
"""
Script para extraer el precio del dólar del BCV (Banco Central de Venezuela)
y guardarlo en un archivo JSON. Diseñado para ejecutarse diariamente a las 6 PM.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import logging
import re
import urllib3

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bcv_scraper.log'),
        logging.StreamHandler()
    ]
)

# Deshabilitar advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BCVDolarScraper:
    def __init__(self):
        self.url = 'https://www.bcv.org.ve/'
        self.alternative_urls = [
            'https://www.bcv.org.ve/',
            'http://www.bcv.org.ve/',
            'https://bcv.org.ve/'
        ]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.data_file = 'precio_dolar_bcv.json'
        
    def get_dolar_price(self):
        """
        Extrae el precio del dólar de la página del BCV
        """
        for url in self.alternative_urls:
            try:
                logging.info(f"Accediendo a {url}")
                response = requests.get(url, headers=self.headers, timeout=60, verify=False)
                response.raise_for_status()
                break
            except Exception as e:
                logging.warning(f"Error con {url}: {e}")
                if url == self.alternative_urls[-1]:  # Si es la última URL
                    raise e
                continue
        
        try:
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Debug: Guardar el HTML para inspección (solo si es necesario)
            # with open('bcv_debug.html', 'w', encoding='utf-8') as f:
            #     f.write(str(soup.prettify()))
            # logging.info("HTML guardado en bcv_debug.html para inspección")
            
            # Buscar el precio del dólar en diferentes posibles ubicaciones
            dolar_price = None
            
            # Método 1: Buscar específicamente en el div con id="dolar"
            dolar_div = soup.find('div', id='dolar')
            if dolar_div:
                # Buscar el precio en el strong dentro del div
                strong_element = dolar_div.find('strong')
                if strong_element:
                    price_text = strong_element.get_text().strip()
                    price_match = re.search(r'[\d,]+\.?\d*', price_text)
                    if price_match:
                        dolar_price = price_match.group()
                        logging.info(f"Precio encontrado en div#dolar: {dolar_price}")
            
            # Método 2: Buscar por texto que contenga "USD" o "Dólar" (fallback)
            if not dolar_price:
                usd_elements = soup.find_all(string=re.compile(r'USD|Dólar|Dollar', re.IGNORECASE))
                for element in usd_elements:
                    parent = element.parent
                    if parent:
                        price_text = parent.get_text()
                        price_match = re.search(r'[\d,]+\.?\d*', price_text)
                        if price_match:
                            dolar_price = price_match.group()
                            break
            
            # Método 2: Buscar en tablas
            if not dolar_price:
                tables = soup.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')
                    for row in rows:
                        cells = row.find_all(['td', 'th'])
                        for cell in cells:
                            cell_text = cell.get_text().strip()
                            if 'USD' in cell_text.upper() or 'DÓLAR' in cell_text.upper():
                                price_match = re.search(r'[\d,]+\.?\d*', cell_text)
                                if price_match:
                                    dolar_price = price_match.group()
                                    break
                        if dolar_price:
                            break
                    if dolar_price:
                        break
            
            # Método 3: Buscar en elementos con clases específicas
            if not dolar_price:
                price_selectors = [
                    '.dolar', '.usd', '.price', '.valor', '.tipo-cambio',
                    '[class*="dolar"]', '[class*="usd"]', '[class*="price"]'
                ]
                
                for selector in price_selectors:
                    elements = soup.select(selector)
                    for element in elements:
                        text = element.get_text().strip()
                        price_match = re.search(r'[\d,]+\.?\d*', text)
                        if price_match:
                            dolar_price = price_match.group()
                            break
                    if dolar_price:
                        break
            
            if dolar_price:
                # Reemplazar coma por punto para formato decimal correcto
                clean_price = dolar_price.replace(',', '.')
                try:
                    price_float = float(clean_price)
                    logging.info(f"Precio del dólar encontrado: {dolar_price}")
                    return price_float
                except ValueError:
                    logging.error(f"No se pudo convertir el precio a número: {dolar_price}")
                    return None
            else:
                logging.warning("No se encontró el precio del dólar en la página")
                return None
                
        except requests.RequestException as e:
            logging.error(f"Error al acceder a la página del BCV: {e}")
            return None
        except Exception as e:
            logging.error(f"Error inesperado: {e}")
            return None
    
    def save_price(self, price):
        """
        Guarda el precio en el archivo JSON
        """
        try:
            data_entry = {
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'precio_dolar': price,
                'timestamp': datetime.now().isoformat()
            }
            
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = []
            
            data.append(data_entry)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            logging.info(f"Precio guardado exitosamente: {price} Bs")
            return True
            
        except Exception as e:
            logging.error(f"Error al guardar el precio: {e}")
            return False
    
    def run(self):
        """
        Ejecuta el proceso completo de extracción y guardado
        """
        logging.info("Iniciando extracción del precio del dólar del BCV")
        
        price = self.get_dolar_price()
        
        if price is not None:
            success = self.save_price(price)
            if success:
                logging.info("Proceso completado exitosamente")
                return True
            else:
                logging.error("Error al guardar el precio")
                return False
        else:
            logging.error("No se pudo obtener el precio del dólar")
            return False

def main():
    """
    Función principal
    """
    scraper = BCVDolarScraper()
    success = scraper.run()
    
    if success:
        print("✅ Precio del dólar extraído y guardado exitosamente")
    else:
        print("❌ Error al extraer el precio del dólar")
        exit(1)

if __name__ == "__main__":
    main()
