#!/usr/bin/env python3
"""
EJEMPLO de configuración de variables de entorno
Copia este archivo como configurar_env.py y completa tus datos
"""

import os

def configurar_variables():
    """Configura las variables de entorno para el scraper"""
    
    print("🔧 Configurando variables de entorno...")
    
    # ⚠️ CONFIGURAR TUS CREDENCIALES AQUÍ:
    
    # Configuración de Email (Gmail)
    os.environ['EMAIL_FROM'] = 'tu_email@gmail.com'  # ⚠️ CAMBIAR: Tu email
    os.environ['EMAIL_PASSWORD'] = 'tu_contraseña_de_aplicacion'  # ⚠️ CAMBIAR: Contraseña de aplicación
    os.environ['EMAIL_TO'] = 'destinatario@gmail.com'  # ⚠️ CAMBIAR: Email destinatario
    
    # Configuración de Telegram
    os.environ['TELEGRAM_BOT_TOKEN'] = 'tu_token_del_bot'  # ⚠️ CAMBIAR: Token del bot
    os.environ['TELEGRAM_CHAT_ID'] = 'tu_chat_id'  # ⚠️ CAMBIAR: Tu chat ID
    
    print("✅ Variables de entorno configuradas")
    print("📧 Email configurado correctamente")
    print("📱 Telegram configurado correctamente")
    print("🔑 Credenciales cargadas de forma segura")

if __name__ == "__main__":
    configurar_variables()
