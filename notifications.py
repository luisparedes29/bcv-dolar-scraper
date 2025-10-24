#!/usr/bin/env python3
"""
Módulo de notificaciones para el scraper del BCV
Soporta notificaciones por email y Telegram
"""

import smtplib
import requests
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Dict, Any
from datetime import datetime
from config import ScraperConfig


def create_email_content(price: float, price_date: str, extraction_time: str) -> str:
    """Crea el contenido del email con información del precio"""
    return f"""
📊 ACTUALIZACIÓN DEL PRECIO DEL DÓLAR BCV

💰 Precio: {price:,.2f} Bs
📅 Fecha del precio: {price_date}
⏰ Extraído el: {extraction_time}
🌍 Zona horaria: {ScraperConfig.TIMEZONE}

---
Este es un mensaje automático del scraper del BCV.
"""


def create_telegram_content(price: float, price_date: str, extraction_time: str) -> str:
    """Crea el contenido del mensaje de Telegram"""
    return f"""📊 *ACTUALIZACIÓN DEL PRECIO DEL DÓLAR BCV*

💰 *Precio:* {price:,.2f} Bs
📅 *Fecha del precio:* {price_date}
⏰ *Extraído el:* {extraction_time}
🌍 *Zona horaria:* {ScraperConfig.TIMEZONE}

---
_Este es un mensaje automático del scraper del BCV._"""


def send_email_notification(price: float, price_date: str, extraction_time: str) -> bool:
    """Envía notificación por email"""
    if not ScraperConfig.EMAIL_ENABLED or not ScraperConfig.is_email_configured():
        logging.warning("Email no configurado o deshabilitado")
        return False
    
    try:
        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = ScraperConfig.EMAIL_FROM
        msg['To'] = ScraperConfig.EMAIL_TO
        msg['Subject'] = ScraperConfig.EMAIL_SUBJECT
        
        # Crear contenido
        body = create_email_content(price, price_date, extraction_time)
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Conectar y enviar
        server = smtplib.SMTP(ScraperConfig.EMAIL_SMTP_SERVER, ScraperConfig.EMAIL_SMTP_PORT)
        server.starttls()
        server.login(ScraperConfig.EMAIL_FROM, ScraperConfig.EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        logging.info("Email enviado exitosamente")
        return True
        
    except Exception as e:
        logging.error(f"Error al enviar email: {e}")
        return False


def send_telegram_notification(price: float, price_date: str, extraction_time: str) -> bool:
    """Envía notificación por Telegram"""
    if not ScraperConfig.TELEGRAM_ENABLED or not ScraperConfig.is_telegram_configured():
        logging.warning("Telegram no configurado o deshabilitado")
        return False
    
    try:
        # Crear URL y datos
        url = f"https://api.telegram.org/bot{ScraperConfig.TELEGRAM_BOT_TOKEN}/sendMessage"
        
        # Crear contenido
        message = create_telegram_content(price, price_date, extraction_time)
        
        data = {
            'chat_id': ScraperConfig.TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        # Enviar mensaje
        response = requests.post(url, data=data, timeout=30)
        response.raise_for_status()
        
        logging.info("Mensaje de Telegram enviado exitosamente")
        return True
        
    except Exception as e:
        logging.error(f"Error al enviar mensaje de Telegram: {e}")
        return False


def send_notifications(price: float, price_date: str, extraction_time: str) -> Dict[str, bool]:
    """Envía todas las notificaciones configuradas"""
    if not ScraperConfig.NOTIFICATIONS_ENABLED:
        logging.info("Notificaciones deshabilitadas")
        return {"email": False, "telegram": False}
    
    results = {}
    
    # Enviar email si está configurado
    if ScraperConfig.EMAIL_ENABLED and ScraperConfig.is_email_configured():
        results["email"] = send_email_notification(price, price_date, extraction_time)
    else:
        results["email"] = False
        logging.info("Email no configurado o deshabilitado")
    
    # Enviar Telegram si está configurado
    if ScraperConfig.TELEGRAM_ENABLED and ScraperConfig.is_telegram_configured():
        results["telegram"] = send_telegram_notification(price, price_date, extraction_time)
    else:
        results["telegram"] = False
        logging.info("Telegram no configurado o deshabilitado")
    
    return results


def test_notifications() -> None:
    """Función de prueba para verificar las notificaciones"""
    test_price = 214.419
    test_date = "2025-10-25 00:00:00"
    test_time = "2025-10-24 17:07:05"
    
    print("🧪 Probando notificaciones...")
    results = send_notifications(test_price, test_date, test_time)
    
    print(f"📧 Email: {'✅ Enviado' if results['email'] else '❌ Error'}")
    print(f"📱 Telegram: {'✅ Enviado' if results['telegram'] else '❌ Error'}")


if __name__ == "__main__":
    # Configurar logging básico
    logging.basicConfig(level=logging.INFO)
    test_notifications()
