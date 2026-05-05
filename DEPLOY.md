# 🚀 Guía Rápida — Deploy en 5 minutos

## ✅ Checklist Pre-Deploy

Antes de empezar, asegúrate de tener:
- [ ] Cuenta en GitHub (https://github.com)
- [ ] Los archivos descargados:
  - `quirkosig_dashboard.py`
  - `requirements.txt`
  - `.streamlit/config.toml`
  - `.gitignore` (opcional pero recomendado)

---

## 📋 Paso a Paso

### 1️⃣ Crear repositorio en GitHub (2 minutos)

1. Ve a https://github.com/new
2. Nombre del repo: `quirkosig-dashboard-v4`
3. Público ✅ (o Privado si prefieres)
4. **NO** marcar "Add a README file"
5. Click en **"Create repository"**

### 2️⃣ Subir archivos (1 minuto)

**Opción A — Desde la web (más fácil):**

1. En tu nuevo repo, click en **"uploading an existing file"**
2. Arrastra estos archivos:
   - `quirkosig_dashboard.py`
   - `requirements.txt`
   - `.gitignore`
3. Click en **"Add file" → "Create new file"**
   - Nombre: `.streamlit/config.toml`
   - Copia el contenido de tu `config.toml`
   - Click "Commit new file"
4. Vuelve al repo y click **"Commit changes"**

**Opción B — Desde terminal:**

```bash
# En la carpeta donde están los archivos
git init
git add .
git commit -m "Dashboard QuirkoSIG v4.0 - 36 meses + T_full dinámico"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/quirkosig-dashboard-v4.git
git push -u origin main
```

### 3️⃣ Deployar en Streamlit Cloud (2 minutos)

1. Ve a **https://share.streamlit.io** (o https://streamlit.io/cloud)
2. Click en **"Sign in with GitHub"**
3. Autoriza a Streamlit acceder a tus repos
4. Click en **"New app"**
5. Completa:
   ```
   Repository: TU_USUARIO/quirkosig-dashboard-v4
   Branch: main
   Main file: quirkosig_dashboard.py
   App URL: quirkosig-v4 (o el nombre que quieras)
   ```
6. Click en **"Deploy!"**

⏳ **Espera 2-3 minutos** mientras se instala...

### 4️⃣ ¡Listo! 🎉

Tu dashboard estará en:
```
https://quirkosig-v4.streamlit.app
```

---

## 📱 Compartir el dashboard

Simplemente copia y pega el link. Cualquiera con el link puede acceder (no necesita cuenta).

---

## 🔄 Actualizar después

1. Edita `quirkosig_dashboard.py` en tu computadora
2. Sube los cambios a GitHub:
   ```bash
   git add quirkosig_dashboard.py
   git commit -m "Actualización: [describe qué cambiaste]"
   git push
   ```
3. **Se actualiza automáticamente** en 1-2 minutos

---

## ⚙️ Configuración Recomendada

En Streamlit Cloud → **Manage app** → **Settings**:

### General
- **App URL:** Puedes cambiarlo en cualquier momento
- **Secrets:** Aquí puedes poner claves API si las necesitas después

### Resources
- **Instance type:** Small es suficiente (gratis)
- **Sleep after inactivity:** Dejar en "Yes" (para plan gratuito)
  - La app "duerme" después de 7 días sin uso
  - Se "despierta" automáticamente cuando alguien la visita

### Advanced
- **Python version:** 3.9 o superior (automático)

---

## 🧪 Probar Localmente Antes de Deployar

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el dashboard
streamlit run quirkosig_dashboard.py

# Se abre automáticamente en http://localhost:8501
```

O usa el script de prueba:
```bash
python test_dashboard.py
```

---

## 🆘 ¿Problemas?

### "App is starting..." por más de 5 minutos
→ Revisa los logs: Manage app → View logs  
→ Verifica que `requirements.txt` está correcto

### Error: "No module named 'streamlit'"
→ Asegúrate que `requirements.txt` está en la raíz del repo  
→ Verifica que el contenido sea exactamente:
```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
```

### Error: "StreamlitAPIException" en sliders
→ Este error ya fue corregido en v4.0  
→ Si lo ves, descarga nuevamente `quirkosig_dashboard.py`

### Los colores no se ven
→ Verifica que `.streamlit/config.toml` esté en la carpeta correcta  
→ Contenido del archivo:
```toml
[theme]
primaryColor="#2E7D32"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#E8F5E9"
textColor="#1A5C28"
font="sans serif"
```

### Los gráficos no cargan
→ Limpiar cache del navegador: Ctrl+Shift+R (Windows/Linux) o Cmd+Shift+R (Mac)  
→ O usar modo incógnito

### Quiero cambiar el nombre de la app
→ Manage app → Settings → General → App URL  
→ El cambio es instantáneo

### La app está lenta
→ Normal en plan gratuito si la app "despertó" recién  
→ Una vez cargada, es rápida por el cache

---

## 🎨 Personalizar Colores

Edita `.streamlit/config.toml`:

```toml
[theme]
primaryColor="#TU_COLOR"        # Color principal (botones, headers)
backgroundColor="#FFFFFF"        # Fondo de la app
secondaryBackgroundColor="#..."  # Fondo del sidebar
textColor="#..."                 # Color del texto
font="sans serif"                # Fuente
```

Colores recomendados:
- Verde QuirkoSIG actual: `#2E7D32`
- Azul corporativo: `#1976D2`
- Gris oscuro: `#424242`

Después de cambiar:
```bash
git add .streamlit/config.toml
git commit -m "Actualizar colores"
git push
```

---

## 📧 Contacto y Soporte

Si algo no funciona, puedes:
1. **Ver logs** en Streamlit Cloud (botón "Manage app" → "Logs")
2. **Preguntar en** https://discuss.streamlit.io
3. **Revisar documentación:** https://docs.streamlit.io

---

## 🎯 Tips Pro

### Hacer que la app se "despierte" más rápido
- Visita la URL al menos una vez a la semana
- O configura un "ping" automático (ej: UptimeRobot)

### Compartir con contraseña
- Requiere plan Team ($20/mes)
- Settings → Visibility → Private
- Puedes invitar usuarios específicos

### Múltiples versiones
- Crea branches en GitHub (`main`, `dev`, `test`)
- Deploya cada branch como una app separada
- Útil para probar cambios sin afectar producción

---

**¡Tu dashboard profesional estará online en menos de 10 minutos!** 🚀

**Versión 4.0 con:**
- ✅ 36 meses de proyección
- ✅ T_full dinámico por revenue
- ✅ Análisis detallado de pagos PT
- ✅ Gráficos interactivos con Plotly
