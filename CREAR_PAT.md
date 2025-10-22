# 🔑 Crear Personal Access Token (PAT) - Guía Paso a Paso

## 📋 Pasos para Crear el PAT

### 1. Ir a GitHub Settings
1. **Haz clic en tu foto de perfil** (esquina superior derecha)
2. **Selecciona "Settings"**

### 2. Acceder a Developer Settings
1. **Scroll hacia abajo** en el menú izquierdo
2. **Haz clic en "Developer settings"** (al final de la lista)

### 3. Crear Personal Access Token
1. **Haz clic en "Personal access tokens"**
2. **Selecciona "Tokens (classic)"**
3. **Haz clic en "Generate new token"**
4. **Selecciona "Generate new token (classic)"**

### 4. Configurar el Token
1. **Note**: `BCV Scraper PAT`
2. **Expiration**: `90 days` (o el tiempo que prefieras)
3. **Scopes**: Marca las siguientes opciones:
   - ✅ **repo** (Full control of private repositories)
   - ✅ **workflow** (Update GitHub Action workflows)

### 5. Generar y Copiar
1. **Haz clic en "Generate token"**
2. **COPIA EL TOKEN INMEDIATAMENTE** (no podrás verlo después)
3. **Guárdalo en un lugar seguro**

## 🔐 Agregar el PAT al Repositorio

### 1. Ir al Repositorio
1. **Ve a tu repositorio**: `https://github.com/luisparedes29/bcv-dolar-scraper`
2. **Haz clic en "Settings"** (pestaña del repositorio)

### 2. Configurar Secret
1. **En el menú izquierdo, haz clic en "Secrets and variables"**
2. **Selecciona "Actions"**
3. **Haz clic en "New repository secret"**

### 3. Agregar el Secret
1. **Name**: `GH_PAT`
2. **Secret**: Pega el token que copiaste
3. **Haz clic en "Add secret"**

## ✅ Verificar Configuración

Después de seguir estos pasos:
1. **El secret `GH_PAT` aparecerá en la lista**
2. **El workflow podrá usar este token para hacer push**
3. **Los permisos estarán configurados correctamente**

## 🚨 Importante

- **Nunca compartas el PAT** con nadie
- **Si se compromete, revócalo inmediatamente**
- **El token expirará según la configuración que elijas**

---

**Una vez completado, el workflow debería funcionar correctamente.**
