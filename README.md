# 🌿 QuirkoSIG — Dashboard Financiero Permanente

Dashboard interactivo para proyecciones financieras con mix de cartera ajustable, 3 escenarios y análisis detallado de pagos por PT.

---

## 🚀 Deploy en Streamlit Cloud (GRATIS y PERMANENTE)

### Paso 1: Preparar los archivos

Necesitas 3 archivos en una carpeta:
- ✅ `quirkosig_dashboard.py` (la app principal)
- ✅ `requirements.txt` (dependencias)
- ✅ Este README (opcional)

### Paso 2: Subir a GitHub

1. **Crear una cuenta en GitHub** (si no tienes): https://github.com
2. **Crear un nuevo repositorio:**
   - Ve a https://github.com/new
   - Nombre: `quirkosig-dashboard` (o el que prefieras)
   - Público o Privado (ambos funcionan)
   - NO marcar "Initialize with README"
   - Click en "Create repository"

3. **Subir los archivos:**
   - Opción fácil (desde la web):
     - En tu repositorio nuevo, click "uploading an existing file"
     - Arrastra `quirkosig_dashboard.py` y `requirements.txt`
     - Click "Commit changes"
   
   - Opción con Git (desde terminal):
     ```bash
     git init
     git add quirkosig_dashboard.py requirements.txt
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin https://github.com/TU_USUARIO/quirkosig-dashboard.git
     git push -u origin main
     ```

### Paso 3: Deployar en Streamlit Cloud

1. **Ir a Streamlit Cloud:** https://streamlit.io/cloud
2. **Iniciar sesión** con tu cuenta de GitHub
3. **Click en "New app"**
4. **Configurar:**
   - Repository: seleccionar `TU_USUARIO/quirkosig-dashboard`
   - Branch: `main`
   - Main file path: `quirkosig_dashboard.py`
   - App URL: elegir un nombre único (ej: `quirkosig-financiero`)
5. **Click en "Deploy"**

⏱️ **Tarda 2-3 minutos** en deployar la primera vez.

### Paso 4: Tu app está ONLINE 🎉

Tu dashboard estará en: `https://TU_NOMBRE-DE-APP.streamlit.app`

- ✅ **Accesible 24/7** desde cualquier dispositivo
- ✅ **Gratis para siempre** (plan Community de Streamlit)
- ✅ **Se actualiza automáticamente** cuando haces cambios en GitHub
- ✅ **Compartible** con un simple link

---

## 🔄 Actualizar el dashboard

1. Editar `quirkosig_dashboard.py` localmente
2. Subir cambios a GitHub:
   ```bash
   git add quirkosig_dashboard.py
   git commit -m "Actualización de parámetros"
   git push
   ```
3. **Streamlit Cloud detecta el cambio y redeploya automáticamente**

---

## 💡 Características del Dashboard

### 📊 5 Secciones principales

1. **Revenue & Flujo de Caja**
   - Revenue mensual comparativo
   - Saldo bancario real
   - Deuda interna con PT
   - Línea de umbral de Sueldo Completo

2. **👥 Pagos PT Individuales** ⭐ CLAVE
   - Cuánto cobra CADA PT mes a mes
   - Acumulado por persona
   - Devengado vs. pagado
   - Líneas de referencia (USD 1.500 y USD 3.000)

3. **🎯 Análisis de Sensibilidad**
   - Simula 4 mix de cartera automáticamente
   - Impacto en revenue y pagos PT
   - Comparación de KPIs

4. **📋 Datos Detallados**
   - Tabla mes a mes con todas las métricas
   - Descarga en CSV
   - Filtrable por escenario

5. **📖 Interpretación**
   - Guía de lectura de los números
   - Qué significa cada métrica
   - Recomendaciones y señales de alarma

### ⚙️ Parámetros Editables (sidebar)

- **Equipo:** honorarios FT, dedicación PT, % no facturable
- **Mix de Cartera:** revenue por CT1/CT2/CT3, % de cada nivel
- **Descuentos:** margen, IIBB, incobrables, lag de cobro
- **Split del margen:** % hacia deuda PT vs. inversión

**Todos los gráficos se actualizan en tiempo real** al cambiar parámetros.

---

## 🎨 Características Profesionales

✅ **Diseño visual:** CSS personalizado con gradientes, cards con colores por escenario  
✅ **Gráficos interactivos:** Zoom, hover, exportar PNG, comparación cruzada  
✅ **Responsive:** Funciona en desktop, tablet y móvil  
✅ **Velocidad:** Cache de cálculos para render instantáneo  
✅ **Exportación:** CSV descargable por escenario  

---

## 📱 Uso en móvil

El dashboard es completamente funcional en celular:
- Sidebar colapsable
- Gráficos adaptables al ancho de pantalla
- Touch-friendly para zoom y pan

---

## 🔒 Privacidad

- **Repositorio público:** cualquiera puede ver el código y usar tu app
- **Repositorio privado:** solo tú ves el código, pero la app es pública por defecto
- Para hacer la app privada: Streamlit Cloud → Settings → Visibility → "Private" (requiere plan Team)

Para uso interno de QuirkoSIG, un repo privado con app pública es suficiente.

---

## ❓ Troubleshooting

**"ModuleNotFoundError" al deployar:**
→ Verificar que `requirements.txt` tiene todas las dependencias

**La app no carga / error 500:**
→ Ver los logs en Streamlit Cloud → Manage app → Logs

**Los gráficos no se ven:**
→ Limpiar cache del navegador

**Quiero cambiar la URL:**
→ Streamlit Cloud → Manage app → Settings → General → App URL

---

## 🆘 Soporte

- **Documentación Streamlit:** https://docs.streamlit.io
- **Community Forum:** https://discuss.streamlit.io
- **Streamlit Cloud docs:** https://docs.streamlit.io/streamlit-community-cloud

---

## 📦 Archivos del paquete

| Archivo | Descripción |
|---------|-------------|
| `quirkosig_dashboard.py` | App principal de Streamlit (490 líneas) |
| `requirements.txt` | Dependencias Python |
| `README.md` | Este archivo |
| `QuirkoSIG_Proyecciones_v3.xlsx` | Modelo Excel completo (opcional, para referencia) |

---

## 🔄 Roadmap futuro

Posibles mejoras:
- [ ] Autenticación para múltiples usuarios
- [ ] Histórico de simulaciones guardadas
- [ ] Comparación con datos reales mes a mes
- [ ] Alertas automáticas por email si hay desviaciones
- [ ] Integración con Google Sheets para actualización de datos reales

---

**Modelo Financiero QuirkoSIG v3.2 · 2025**  
*Dashboard deployado con Streamlit Cloud*
