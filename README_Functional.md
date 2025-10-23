# 🎯 BCV Scraper - Paradigma Funcional

Este proyecto ha sido refactorizado para usar **paradigma funcional** en lugar de orientado a objetos, resultando en código más simple, directo y fácil de entender.

## 🚀 Principios Funcionales Aplicados

### ✅ **Funciones Puras**
- Sin efectos secundarios
- Mismo input siempre produce mismo output
- No modifican estado externo

### ✅ **Inmutabilidad**
- Los datos no se modifican, se transforman
- Nuevas estructuras en lugar de mutar existentes

### ✅ **Composición de Funciones**
- Funciones pequeñas que se combinan
- Código más modular y reutilizable

### ✅ **Sin Estado Mutable**
- No hay clases con estado
- Configuración como constantes

## 📁 Estructura del Proyecto

```
ProyectoBCV/
├── bcv_scraper.py              # ✅ Script principal (Funcional)
├── functional_utils.py         # ✅ Utilidades funcionales
├── bcv_scraper_oop.py         # 📦 Versión OOP (respaldo)
├── bcv_scraper_original.py    # 📦 Script original (respaldo)
├── ejecutar.bat               # ✅ Script de ejecución
└── [archivos de datos y logs]
```

## 🔧 Funciones Principales

### **Flujo Principal**
```python
def extract_and_save_price() -> bool:
    """Función principal que extrae y guarda el precio"""
    soup = fetch_page_content()           # 1. Obtener HTML
    price = find_dollar_price(soup)       # 2. Extraer precio
    return save_dollar_price(price)      # 3. Guardar datos
```

### **Estrategias de Búsqueda**
```python
# Múltiples estrategias funcionales
search_strategies = [
    search_in_dollar_div,      # Div específico
    search_in_usd_text,        # Texto con USD
    search_in_tables,          # Tablas HTML
    search_with_css_selectors  # Selectores CSS
]
```

### **Transformación de Datos**
```python
def create_price_entry(price: float) -> Dict[str, Any]:
    """Crea entrada de datos (inmutable)"""
    now = get_venezuela_time()
    return {
        'fecha': format_timestamp(now),
        'precio_dolar': price,
        'timestamp': get_iso_timestamp(now),
        'zona_horaria': f'{TIMEZONE} (UTC-4)'
    }
```

## 🎯 Ventajas del Paradigma Funcional

### **Antes (OOP)**
```python
class BCVDollarScraper:
    def __init__(self):
        self.web_scraper = WebScraper()
        self.price_finder = DollarPriceFinder()
        self.data_storage = DataStorage()
    
    def run(self):
        # Lógica compleja con estado
```

### **Después (Funcional)**
```python
def extract_and_save_price() -> bool:
    """Función pura sin estado"""
    soup = fetch_page_content()
    price = find_dollar_price(soup)
    return save_dollar_price(price)
```

## 🔄 Comparación de Paradigmas

| Aspecto | OOP | Funcional |
|---------|-----|-----------|
| **Complejidad** | Clases, herencia, estado | Funciones simples |
| **Testing** | Mocking de objetos | Funciones puras |
| **Debugging** | Estado mutable | Flujo de datos claro |
| **Mantenimiento** | Acoplamiento | Bajo acoplamiento |
| **Legibilidad** | Verboso | Directo y claro |

## 🧪 Funciones de Utilidad

### **Composición de Funciones**
```python
# Composición de funciones
def compose(*functions):
    """Composición de derecha a izquierda"""
    def composed(x):
        return reduce(lambda acc, f: f(acc), reversed(functions), x)
    return composed

# Uso
parse_price = compose(parse_price_to_float, extract_price_from_text)
```

### **Funciones de Transformación**
```python
# Transformación inmutable
def append_to_list(item):
    """Agrega elemento sin mutar lista original"""
    return lambda lst: lst + [item]

# Uso
new_data = append_to_list(price_entry)(existing_data)
```

### **Funciones de Validación**
```python
def is_valid_price(price: Optional[float]) -> bool:
    """Valida precio de forma pura"""
    return price is not None and price > 0
```

## 🚀 Cómo Usar

### **Ejecución Simple**
```bash
python bcv_scraper.py
```

### **Ejecución con Batch**
```bash
ejecutar.bat
```

## 📊 Beneficios Obtenidos

### ✅ **Simplicidad**
- Código más directo y fácil de entender
- Sin conceptos complejos de OOP
- Flujo de datos claro

### ✅ **Testabilidad**
- Funciones puras fáciles de testear
- Sin dependencias externas
- Resultados predecibles

### ✅ **Mantenibilidad**
- Funciones pequeñas y específicas
- Bajo acoplamiento
- Fácil de modificar

### ✅ **Performance**
- Sin overhead de objetos
- Funciones optimizables
- Menos memoria

## 🔧 Funciones de Utilidad Disponibles

### **Manejo de Texto**
- `clean_text()`: Limpia texto
- `contains_any_keyword()`: Busca palabras clave
- `extract_price_from_text()`: Extrae precios

### **Manejo de Fechas**
- `get_venezuela_time()`: Hora de Venezuela
- `format_timestamp()`: Formatea fechas
- `get_iso_timestamp()`: Timestamp ISO

### **Transformación de Datos**
- `create_price_entry()`: Crea entrada de datos
- `append_to_list()`: Agrega a lista (inmutable)
- `validate_price_data()`: Valida datos

### **Composición**
- `compose()`: Composición de funciones
- `pipe()`: Pipe de funciones
- `try_strategies()`: Prueba múltiples estrategias

## 🎯 Flujo de Datos

```
Input (URL) 
    ↓
fetch_page_content() 
    ↓
find_dollar_price() 
    ↓
save_dollar_price() 
    ↓
Output (Success/Failure)
```

## 📝 Conclusión

El paradigma funcional ha resultado en:

- **Código más simple** y directo
- **Funciones puras** fáciles de testear
- **Inmutabilidad** que previene bugs
- **Composición** que facilita reutilización
- **Flujo de datos claro** y predecible

¡El script mantiene toda su funcionalidad pero ahora es más funcional y elegante! 🎉
