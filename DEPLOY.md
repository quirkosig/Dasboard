# 🚀 Guía Rápida — Deploy en 5 minutos

## ✅ Checklist Pre-Deploy

Antes de empezar, asegúrate de tener:
- [ ] Cuenta en GitHub (https://github.com)
- [ ] Los 3 archivos descargados:
  - `quirkosig_dashboard.py`
  - `requirements.txt`
  - `.streamlit/config.toml`

---

## 📋 Paso a Paso

### 1️⃣ Crear repositorio en GitHub (2 minutos)

1. Ve a https://github.com/new
2. Nombre del repo: `quirkosig-dashboard`
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
3. Crea una carpeta `.streamlit` y sube `config.toml` dentro
4. Click en **"Commit changes"**

**Opción B — Desde terminal:**

```bash
# En la carpeta donde están los archivos
git init
git add .
git commit -m "Dashboard QuirkoSIG v3.2"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/quirkosig-dashboard.git
git push -u origin main
```

### 3️⃣ Deployar en Streamlit Cloud (2 minutos)

1. Ve a **https://share.streamlit.io** (o https://streamlit.io/cloud)
2. Click en **"Sign in with GitHub"**
3. Autoriza a Streamlit acceder a tus repos
4. Click en **"New app"**
5. Completa:
   ```
   Repository: TU_USUARIO/quirkosig-dashboard
   Branch: main
   Main file: quirkosig_dashboard.py
   App URL: quirkosig-financiero (o el nombre que quieras)
   ```
6. Click en **"Deploy!"**

⏳ **Espera 2-3 minutos** mientras se instala...

### 4️⃣ ¡Listo! 🎉

Tu dashboard estará en:
```
https://quirkosig-financiero.streamlit.app
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
   git commit -m "Actualización"
   git push
   ```
3. **Se actualiza automáticamente** en 1-2 minutos

---

## ⚙️ Configuración Recomendada

En Streamlit Cloud → **Manage app** → **Settings**:

- **Sleep after inactivity:** Dejar en "Yes" (para plan gratuito)
- **Secrets:** Aquí puedes poner claves API si las necesitas después
- **Resources:** Small instance es suficiente

---

## 🆘 ¿Problemas?

**"App is starting..." por más de 5 minutos**
→ Revisa los logs: Manage app → View logs

**Error: "No module named 'streamlit'"**
→ Asegúrate que `requirements.txt` está en la raíz del repo

**Error: "StreamlitAPIException" en sliders**
→ Este error ya fue corregido en la última versión. Si lo ves:
   - Descarga nuevamente `quirkosig_dashboard.py`
   - El problema era que IIBB usaba `(0, 5, 3.5)` en vez de `(0.0, 5.0, 3.5)`
   - Sube la versión corregida a GitHub

**Los colores no se ven**
→ Verifica que `.streamlit/config.toml` esté en la carpeta correcta

**Quiero cambiar el nombre de la app**
→ Manage app → Settings → General → App URL

**🧪 Probar antes de deployar**
→ Ejecuta `python test_dashboard.py` para verificar que todo está bien

---

## 📧 Contacto

Si algo no funciona, puedes:
1. Ver logs en Streamlit Cloud
2. Preguntar en https://discuss.streamlit.io
3. Revisar la documentación: https://docs.streamlit.io

---

**¡Tu dashboard profesional estará online en menos de 10 minutos!** 🚀
