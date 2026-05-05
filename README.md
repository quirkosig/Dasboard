# 🌿 QuirkoSIG — Dashboard Financiero v4

Dashboard interactivo para proyecciones financieras a **36 meses** con **T_full dinámico** basado en revenue real.

---

## 🆕 Novedades de la Versión 4

### Cambios principales vs v3:

| Característica | v3 (anterior) | v4 (actual) |
|----------------|---------------|-------------|
| **Proyección** | 24 meses | **36 meses** (3 años) |
| **T_full** | Mes fijo (15) | **Dinámico** (cuando cobros ≥ USD 18,000) |
| **FT inicial** | USD 3,000 desde inicio | **USD 2,500** hasta alcanzar umbral |
| **Mandatorio** | USD 3,600 fijo | **USD 3,000 → USD 14,400** (dinámico) |
| **PT → FT** | Mes fijo | **Solo cuando revenue lo permite** |

### Por qué importa:

- ✅ **Más realista:** Los PT no cobran como FT hasta que hay revenue suficiente
- ✅ **Mejor planificación:** 36 meses de visibilidad vs 24
- ✅ **Decisiones fundadas:** Sabes CUÁNDO y no solo "si" alcanzas T_full
- ✅ **Saldo banco preciso:** Refleja costos reales sin inflación artificial

---

## 🚀 Deploy en Streamlit Cloud (GRATIS y PERMANENTE)

### Paso 1: Preparar los archivos

Necesitas 3 archivos en una carpeta:
- ✅ `quirkosig_dashboard.py` (la app principal)
- ✅ `requirements.txt` (dependencias)
- ✅ `.streamlit/config.toml` (configuración de tema)

### Paso 2: Subir a GitHub

1. **Crear una cuenta en GitHub** (si no tienes): https://github.com
2. **Crear un nuevo repositorio:**
   - Ve a https://github.com/new
   - Nombre: `quirkosig-dashboard-v4` (o el que prefieras)
   - Público o Privado (ambos funcionan)
   - NO marcar "Initialize with README"
   - Click en "Create repository"

3. **Subir los archivos:**
   
   **Opción fácil (desde la web):**
   - En tu repositorio nuevo, click "uploading an existing file"
   - Arrastra `quirkosig_dashboard.py`, `requirements.txt`, y `.gitignore`
   - Crea una carpeta `.streamlit` y sube `config.toml` dentro
   - Click "Commit changes"
   
   **Opción con Git (desde terminal):**
   ```bash
   git init
   git add quirkosig_dashboard.py requirements.txt .gitignore
   mkdir .streamlit
   # Copia config.toml a .streamlit/
   git add .streamlit/config.toml
   git commit -m "Dashboard QuirkoSIG v4.0"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/quirkosig-dashboard-v4.git
   git push -u origin main
   ```

### Paso 3: Deployar en Streamlit Cloud

1. **Ir a Streamlit Cloud:** https://streamlit.io/cloud
2. **Iniciar sesión** con tu cuenta de GitHub
3. **Click en "New app"**
4. **Configurar:**
   - Repository: seleccionar `TU_USUARIO/quirkosig-dashboard-v4`
   - Branch: `main`
   - Main file path: `quirkosig_dashboard.py`
   - App URL: elegir un nombre único (ej: `quirkosig-v4`)
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

## 💡 Características del Dashboard v4

### 📊 5 Secciones principales

#### 1. **Revenue & Flujo de Caja**
   - Revenue mensual comparativo (3 escenarios)
   - Saldo bancario real
   - Deuda interna con PT
   - **Línea de umbral de Sueldo Completo** (USD 18,000)

#### 2. **👥 Pagos PT Individuales** ⭐ CLAVE
   - Cuánto cobra **CADA PT** mes a mes (no el total)
   - Acumulado por persona
   - Devengado vs. pagado
   - Líneas de referencia:
     - PT@50%: USD 1,500
     - PT@75%: USD 2,250
     - FT: USD 3,000

#### 3. **🎯 Análisis de Sensibilidad**
   - Simula 4 mix de cartera automáticamente
   - Impacto en revenue y pagos PT
   - Comparación de KPIs mes 36

#### 4. **📋 Datos Detallados**
   - Tabla mes a mes con todas las métricas
   - Descarga en CSV
   - Filtrable por escenario

#### 5. **📖 Interpretación**
   - Guía de lectura de los números
   - Qué significa cada métrica
   - Recomendaciones y señales de alarma

### ⚙️ Parámetros Editables (sidebar)

**Equipo:**
- Honorarios FT, dedicación PT@50%/75%, % no facturable, overhead

**Mix de Cartera:**
- Revenue por CT1/CT2/CT3
- % de cada nivel

**Descuentos:**
- Margen, IIBB, incobrables, lag de cobro

**Split del margen:**
- % hacia deuda PT vs. inversión

**Escenario Base:**
- Utilización inicial (10%)
- Crecimiento mensual (5.5%)
- T_mid (mes 8: PT@50% → PT@75%)
- Anticipo inicial (USD 5,000)

**Todos los gráficos se actualizan en tiempo real** al cambiar parámetros.

---

## 🎨 Características Profesionales

✅ **Diseño visual:** CSS personalizado con gradientes, cards con colores por escenario  
✅ **Gráficos interactivos:** Zoom, hover, exportar PNG, comparación cruzada  
✅ **Responsive:** Funciona en desktop, tablet y móvil  
✅ **Velocidad:** Cache de cálculos para render instantáneo  
✅ **Exportación:** CSV descargable por escenario  

---

## 📊 KPIs Principales Mostrados (mes 36)

| Escenario | Saldo Banco | PT Acum/PT | Revenue | T_full Real |
|-----------|:-----------:|:----------:|:-------:|:-----------:|
| **Conservador** | -$27,475 | $5,011 | $5,540 | ❌ Nunca |
| **Base** | **$40,102** ✅ | **$79,939** ✅ | $28,140 | **Mes 28** |
| **Optimista** | $562,537 | $96,750 | $61,440 | Mes 12 |

---

## 🎯 Decisiones Estratégicas que el Dashboard Responde

1. **¿Cuándo podemos pasar los 3 PT a FT?**
   → Cuando cobros mensuales alcancen USD 18,000

2. **¿Qué mix de cartera necesitamos para ser viables?**
   → Simula en la tab "Sensibilidad"

3. **¿Es viable empezar con 10% utilización?**
   → Revisa saldo mes 36 en escenario Base

4. **¿Cuánto acumula cada PT en 3 años?**
   → Ver "PT Acum/PT" mes 36 (Base: USD 79,939)

5. **¿Cuánto antes llegamos a T_full si mejoramos growth?**
   → Ajusta "Crecimiento mensual" en sidebar y observa

---

## 📱 Uso en móvil

El dashboard es completamente funcional en celular:
- Sidebar colapsable
- Gráficos adaptables al ancho de pantalla
- Touch-friendly para zoom y pan
- Todos los parámetros editables desde móvil

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
→ Limpiar cache del navegador o usar modo incógnito

**Quiero cambiar la URL:**
→ Streamlit Cloud → Manage app → Settings → General → App URL

**🧪 Probar antes de deployar:**
→ Ejecuta `python test_dashboard.py` para verificar que todo está bien

---

## 🆘 Soporte

- **Documentación Streamlit:** https://docs.streamlit.io
- **Community Forum:** https://discuss.streamlit.io
- **Streamlit Cloud docs:** https://docs.streamlit.io/streamlit-community-cloud

---

## 📦 Archivos del paquete

| Archivo | Descripción |
|---------|-------------|
| `quirkosig_dashboard.py` | App principal de Streamlit (~750 líneas) |
| `requirements.txt` | Dependencias Python |
| `.streamlit/config.toml` | Tema verde personalizado |
| `test_dashboard.py` | Script de prueba pre-deploy |
| `README.md` | Este archivo |
| `DEPLOY.md` | Guía rápida de deploy |
| `.gitignore` | Archivos a ignorar en Git |

---

## 🔄 Roadmap futuro

Posibles mejoras:
- [ ] Autenticación para múltiples usuarios
- [ ] Histórico de simulaciones guardadas
- [ ] Comparación con datos reales mes a mes
- [ ] Alertas automáticas por email si hay desviaciones
- [ ] Integración con Google Sheets para actualización de datos reales
- [ ] Simulación Monte Carlo para escenarios probabilísticos

---

## 📝 Changelog

### v4.0 (Mayo 2025)
- ✨ Proyección extendida a 36 meses
- ✨ T_full dinámico basado en revenue real
- ✨ FT inicial USD 2,500 (no USD 3,000)
- ✨ Mandatorio crece automáticamente de USD 3,000 a USD 14,400
- ✨ PT pasan a FT solo cuando revenue lo permite
- 🐛 Corregido: saldo banco ya no se infla artificialmente
- 🐛 Corregido: PT siguen cobrando después de alcanzar T_full

### v3.2 (Marzo 2025)
- Modelo original a 24 meses con T_full fijo

---

**Modelo Financiero QuirkoSIG v4.0 · Mayo 2025**  
*Dashboard deployado con Streamlit Cloud*
