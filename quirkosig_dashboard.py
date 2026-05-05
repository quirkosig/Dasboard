#!/usr/bin/env python3
"""
🌿 QuirkoSIG — Dashboard Financiero Interactivo v4
Proyecciones a 36 meses con T_full dinámico y análisis detallado de pagos PT

Modelo actualizado con:
- 36 meses de proyección (3 años completos)
- T_full dinámico basado en revenue (≥ USD 18,000/mes)
- FT inicial cobra USD 2,500 hasta alcanzar umbral
- Mandatorio se expande de USD 3,000 a USD 14,400 cuando corresponde
- Análisis detallado mes a mes de cada PT

Autor: Claude + QuirkoSIG
Versión: 4.0
Fecha: Mayo 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================================

st.set_page_config(
    page_title="QuirkoSIG Dashboard v4",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS PERSONALIZADO
# ============================================================================

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #2E7D32;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .scenario-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .badge-conservador { background: #4472C4; color: white; }
    .badge-base { background: #70AD47; color: white; }
    .badge-optimista { background: #ED7D31; color: white; }
    .warning-box {
        background: #FFF3CD;
        border-left: 4px solid #FFC107;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .success-box {
        background: #D4EDDA;
        border-left: 4px solid #28A745;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .info-box {
        background: #D1ECF1;
        border-left: 4px solid #17A2B8;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCIONES DE CÁLCULO DEL MODELO
# ============================================================================

@st.cache_data
def calcular_modelo(params):
    """
    Calcula las proyecciones financieras para 36 meses.
    
    Modelo v4 con:
    - T_full dinámico (cuando cobros >= USD 18,000)
    - FT inicial USD 2,500
    - Mandatorio crece de USD 3,000 a USD 14,400
    """
    
    # Parámetros del modelo
    meses = 36
    
    # Revenue unitario por tipo de contrato
    rev_ct1 = params['rev_ct1']
    rev_ct2 = params['rev_ct2']
    rev_ct3 = params['rev_ct3']
    
    # Mix de cartera
    mix_ct1 = params['mix_ct1'] / 100
    mix_ct2 = params['mix_ct2'] / 100
    mix_ct3 = params['mix_ct3'] / 100
    
    # Revenue promedio ponderado
    rev_u = rev_ct1 * mix_ct1 + rev_ct2 * mix_ct2 + rev_ct3 * mix_ct3
    
    # Parámetros de equipo
    honorario_ft = params['honorario_ft']
    ded_pt_50 = params['ded_pt_50'] / 100
    ded_pt_75 = params['ded_pt_75'] / 100
    no_fact = params['no_facturable'] / 100
    
    # Overhead
    oh = params['overhead'] / 100
    
    # Descuentos
    margen_pct = params['margen'] / 100
    iibb_pct = params['iibb'] / 100
    incob_pct = params['incobrables'] / 100
    lag_cobro = params['lag_cobro']
    
    # Split margen
    margen_a_deuda = params['margen_a_deuda'] / 100
    
    # Umbrales
    umbral_sc = 4 * honorario_ft * (1 + oh) / 0.8  # ~USD 18,000
    
    # Resultados por escenario
    resultados = {}
    
    escenarios = {
        'Conservador': {
            'util_ini': 0.05,
            'crec': 0.04,
            'util_max': 0.60,
            't_mid': 18,
            'anticipo': 1500
        },
        'Base': {
            'util_ini': params['util_ini_base'] / 100,
            'crec': params['crec_base'] / 100,
            'util_max': 0.75,
            't_mid': params['t_mid_base'],
            'anticipo': params['anticipo_base']
        },
        'Optimista': {
            'util_ini': 0.25,
            'crec': 0.075,
            'util_max': 0.80,
            't_mid': 5,
            'anticipo': 6000
        }
    }
    
    for nombre_esc, esc in escenarios.items():
        # Inicializar arrays
        mes_num = np.arange(1, meses + 1)
        
        # Capacidad (asumiendo 1 FT + 3 PT)
        capacidad_base = 1.0  # 1 FT
        
        # Utilización
        util = np.minimum(
            esc['util_ini'] * (1 + esc['crec']) ** (mes_num - 1),
            esc['util_max']
        )
        
        # Dedicación PT por mes
        dedicacion_pt = np.where(
            mes_num >= esc['t_mid'],
            ded_pt_75,
            ded_pt_50
        )
        
        # Capacidad total = 1 FT + 3 PT * dedicación
        capacidad = capacidad_base + 3 * dedicacion_pt
        
        # Units facturable
        units = capacidad * util
        
        # Revenue bruto
        revenue_bruto = units * rev_u
        
        # Revenue neto (después de IIBB e incobrables)
        revenue_neto = revenue_bruto * (1 - iibb_pct) * (1 - incob_pct)
        
        # Cobros (con lag)
        cobros = np.zeros(meses)
        cobros[0] = esc['anticipo']
        for m in range(1, meses):
            if m > lag_cobro:
                cobros[m] = revenue_neto[m - lag_cobro - 1]
        
        # MAX cobros acumulado (para T_full dinámico)
        max_cobros = np.maximum.accumulate(cobros)
        
        # T_full alcanzado cuando max_cobros >= umbral
        t_full_alcanzado = max_cobros >= umbral_sc
        
        # Mandatorio
        # Antes del umbral: 1 FT × USD 2,500 × OH = USD 3,000
        # Después: 4 FT × USD 3,000 × OH = USD 14,400
        mandatorio = np.where(
            t_full_alcanzado,
            4 * honorario_ft * (1 + oh),
            2500 * (1 + oh)
        )
        
        # Costos = 80% de cobros
        costos_80 = cobros * 0.8
        
        # Excedente
        excedente = np.maximum(0, costos_80 - mandatorio)
        
        # Margen = 20% de cobros
        margen = cobros * margen_pct
        
        # PT_dev (devengado a PT)
        # Antes del umbral: según dedicación
        # Después: 0 (ya son FT, cobran del Mandatorio)
        pt_dev = np.where(
            t_full_alcanzado,
            0,
            3 * honorario_ft * dedicacion_pt
        )
        
        # Deuda PT (acumulativa)
        deuda_pt = np.zeros(meses)
        mg_a_deuda = np.zeros(meses)
        pt_pag = np.zeros(meses)
        
        for m in range(meses):
            if m == 0:
                deuda_ant = 0
            else:
                deuda_ant = deuda_pt[m-1]
            
            # Margen que va a deuda (40% del margen si hay deuda)
            if deuda_ant > 0 or pt_dev[m] > excedente[m]:
                mg_a_deuda[m] = margen[m] * margen_a_deuda
            
            # PT pago
            pt_pag[m] = min(excedente[m] + mg_a_deuda[m], pt_dev[m] + deuda_ant)
            
            # Deuda nueva
            deuda_pt[m] = deuda_ant + pt_dev[m] - pt_pag[m]
        
        # Margen a inversión
        mg_a_inv = margen - mg_a_deuda
        
        # Fondo de inversión (acumulado)
        fondo_inv = np.cumsum(mg_a_inv)
        
        # Saldo banco
        saldo = np.zeros(meses)
        for m in range(meses):
            if m == 0:
                saldo_ant = 0
            else:
                saldo_ant = saldo[m-1]
            
            saldo[m] = saldo_ant + cobros[m] - mandatorio[m] - pt_pag[m]
        
        # PT Individual (cada uno de los 3 PT)
        pt_dev_cada_uno = np.where(
            t_full_alcanzado,
            honorario_ft,  # USD 3,000 como FT
            pt_dev / 3
        )
        
        pt_pag_cada_uno = np.where(
            t_full_alcanzado,
            honorario_ft + pt_pag / 3,  # USD 3,000 + pago deuda residual
            pt_pag / 3
        )
        
        pt_acum_cada_uno = np.cumsum(pt_pag_cada_uno)
        
        # Guardar resultados
        resultados[nombre_esc] = pd.DataFrame({
            'Mes': mes_num,
            'Utilización': util,
            'Dedicación PT': dedicacion_pt,
            'Capacidad': capacidad,
            'Units': units,
            'Revenue Bruto': revenue_bruto,
            'Revenue Neto': revenue_neto,
            'Cobros': cobros,
            'MAX Cobros': max_cobros,
            'T_full Alcanzado': t_full_alcanzado,
            'Mandatorio': mandatorio,
            'Excedente': excedente,
            'Margen': margen,
            'PT_dev': pt_dev,
            'PT_pag': pt_pag,
            'Deuda PT': deuda_pt,
            'Mg→Deuda': mg_a_deuda,
            'Mg→Inv': mg_a_inv,
            'Fondo Inv': fondo_inv,
            'Saldo Banco': saldo,
            'PT Dev/PT': pt_dev_cada_uno,
            'PT Pag/PT': pt_pag_cada_uno,
            'PT Acum/PT': pt_acum_cada_uno,
        })
    
    return resultados, umbral_sc

# ============================================================================
# PARÁMETROS POR DEFECTO
# ============================================================================

def get_default_params():
    return {
        # Revenue unitario
        'rev_ct1': 5000,
        'rev_ct2': 10000,
        'rev_ct3': 10000,
        # Mix de cartera
        'mix_ct1': 20,
        'mix_ct2': 60,
        'mix_ct3': 20,
        # Equipo
        'honorario_ft': 3000,
        'ded_pt_50': 50,
        'ded_pt_75': 75,
        'no_facturable': 10,
        'overhead': 20,
        # Descuentos
        'margen': 20,
        'iibb': 3.5,
        'incobrables': 5,
        'lag_cobro': 2,
        # Split margen
        'margen_a_deuda': 40,
        # Escenario Base
        'util_ini_base': 10,
        'crec_base': 5.5,
        't_mid_base': 8,
        'anticipo_base': 5000,
    }

# ============================================================================
# SIDEBAR — PARÁMETROS
# ============================================================================

st.sidebar.markdown("## ⚙️ Parámetros del Modelo")

params = {}

with st.sidebar.expander("💼 Revenue Unitario", expanded=False):
    params['rev_ct1'] = st.number_input("CT1 (proyectos pequeños)", 1000, 20000, 5000, 500)
    params['rev_ct2'] = st.number_input("CT2 (proyectos medianos)", 1000, 30000, 10000, 500)
    params['rev_ct3'] = st.number_input("CT3 (proyectos grandes)", 1000, 30000, 10000, 500)

with st.sidebar.expander("📊 Mix de Cartera", expanded=False):
    params['mix_ct1'] = st.slider("% CT1", 0, 100, 20, 5)
    params['mix_ct2'] = st.slider("% CT2", 0, 100, 60, 5)
    params['mix_ct3'] = st.slider("% CT3", 0, 100, 20, 5)
    
    total_mix = params['mix_ct1'] + params['mix_ct2'] + params['mix_ct3']
    if total_mix != 100:
        st.warning(f"⚠️ Total: {total_mix}% (debe ser 100%)")

with st.sidebar.expander("👥 Equipo", expanded=False):
    params['honorario_ft'] = st.number_input("Honorario FT objetivo (USD)", 2000, 5000, 3000, 100)
    params['ded_pt_50'] = st.slider("Dedicación PT@50% (%)", 30, 70, 50, 5)
    params['ded_pt_75'] = st.slider("Dedicación PT@75% (%)", 50, 90, 75, 5)
    params['no_facturable'] = st.slider("% No facturable", 0, 30, 10, 1)
    params['overhead'] = st.slider("Overhead (%)", 10, 40, 20, 1)

with st.sidebar.expander("💰 Descuentos", expanded=False):
    params['margen'] = st.slider("Margen (% del revenue)", 10, 30, 20, 1)
    params['iibb'] = st.slider("IIBB (%)", 0.0, 10.0, 3.5, 0.1)
    params['incobrables'] = st.slider("Incobrables (%)", 0, 15, 5, 1)
    params['lag_cobro'] = st.slider("Lag de cobro (meses)", 0, 6, 2, 1)

with st.sidebar.expander("🎯 Split Margen", expanded=False):
    params['margen_a_deuda'] = st.slider("% Margen → Deuda PT", 0, 100, 40, 5)
    st.caption(f"{100 - params['margen_a_deuda']}% va a Fondo de Inversión")

with st.sidebar.expander("📈 Escenario BASE", expanded=True):
    params['util_ini_base'] = st.slider("Utilización inicial (%)", 5, 30, 10, 1)
    params['crec_base'] = st.slider("Crecimiento mensual (%)", 3.0, 10.0, 5.5, 0.1)
    params['t_mid_base'] = st.slider("T_mid (mes PT@50% → PT@75%)", 4, 12, 8, 1)
    params['anticipo_base'] = st.number_input("Anticipo inicial (USD)", 0, 10000, 5000, 500)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Restaurar valores por defecto"):
    st.rerun()

# ============================================================================
# CALCULAR MODELO
# ============================================================================

resultados, umbral_sc = calcular_modelo(params)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class="main-header">
    <h1>🌿 QuirkoSIG — Dashboard Financiero v4</h1>
    <p style="font-size: 1.1rem; margin-top: 0.5rem; opacity: 0.95;">
        Proyecciones a 36 meses con T_full dinámico basado en revenue
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# KPIs PRINCIPALES
# ============================================================================

st.markdown("## 🎯 KPIs Principales — Mes 36")

col1, col2, col3 = st.columns(3)

for idx, (nombre, color, badge) in enumerate([
    ('Conservador', '#4472C4', 'badge-conservador'),
    ('Base', '#70AD47', 'badge-base'),
    ('Optimista', '#ED7D31', 'badge-optimista')
]):
    df = resultados[nombre]
    mes_36 = df.iloc[-1]
    
    # Encontrar mes donde se alcanzó T_full
    t_full_mes = df[df['T_full Alcanzado']]['Mes'].min() if df['T_full Alcanzado'].any() else None
    
    with [col1, col2, col3][idx]:
        st.markdown(f'<span class="scenario-badge {badge}">{nombre}</span>', unsafe_allow_html=True)
        
        st.metric("Saldo Banco", f"${mes_36['Saldo Banco']:,.0f}")
        st.metric("PT Acumulado/PT", f"${mes_36['PT Acum/PT']:,.0f}")
        st.metric("Revenue Mensual", f"${mes_36['Revenue Neto']:,.0f}")
        
        if t_full_mes:
            st.success(f"✅ T_full alcanzado: **Mes {int(t_full_mes)}**")
        else:
            st.warning("⚠️ T_full **no alcanzado** en 36 meses")

st.markdown(f"""
<div class="info-box">
    <strong>💡 Umbral de Sueldo Completo (SC):</strong> USD {umbral_sc:,.0f}/mes<br>
    Cuando los cobros mensuales alcanzan este umbral, el Mandatorio crece de USD 3,000 a USD 14,400 
    y los 3 PT pasan a cobrar como FT (USD 3,000/mes cada uno).
</div>
""", unsafe_allow_html=True)

# ============================================================================
# TAB Navigation
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Revenue & Flujo",
    "👥 Pagos PT Individual",
    "🎯 Análisis Sensibilidad",
    "📋 Datos Detallados",
    "📖 Interpretación"
])

# ============================================================================
# TAB 1: REVENUE & FLUJO DE CAJA
# ============================================================================

with tab1:
    st.markdown("## 📈 Revenue y Flujo de Caja")
    
    # Gráfico Revenue Mensual
    fig_rev = go.Figure()
    
    colors_map = {'Conservador': '#4472C4', 'Base': '#70AD47', 'Optimista': '#ED7D31'}
    
    for nombre in ['Conservador', 'Base', 'Optimista']:
        df = resultados[nombre]
        fig_rev.add_trace(go.Scatter(
            x=df['Mes'],
            y=df['Revenue Neto'],
            name=nombre,
            line=dict(color=colors_map[nombre], width=2),
            mode='lines'
        ))
    
    # Línea de umbral SC
    fig_rev.add_hline(
        y=umbral_sc,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Umbral SC: ${umbral_sc:,.0f}",
        annotation_position="right"
    )
    
    fig_rev.update_layout(
        title="Revenue Mensual Neto por Escenario",
        xaxis_title="Mes",
        yaxis_title="USD",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig_rev, use_container_width=True)
    
    # Gráfico Saldo Bancario
    fig_saldo = go.Figure()
    
    for nombre in ['Conservador', 'Base', 'Optimista']:
        df = resultados[nombre]
        fig_saldo.add_trace(go.Scatter(
            x=df['Mes'],
            y=df['Saldo Banco'],
            name=nombre,
            line=dict(color=colors_map[nombre], width=2),
            mode='lines',
            fill='tozeroy' if nombre == 'Base' else None
        ))
    
    fig_saldo.add_hline(y=0, line_color="gray", line_dash="dot")
    
    fig_saldo.update_layout(
        title="⚠️ Saldo Bancario Real",
        xaxis_title="Mes",
        yaxis_title="USD",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig_saldo, use_container_width=True)
    
    # Gráfico Deuda PT
    fig_deuda = go.Figure()
    
    for nombre in ['Conservador', 'Base', 'Optimista']:
        df = resultados[nombre]
        fig_deuda.add_trace(go.Scatter(
            x=df['Mes'],
            y=df['Deuda PT'],
            name=nombre,
            line=dict(color=colors_map[nombre], width=2),
            mode='lines'
        ))
    
    fig_deuda.update_layout(
        title="Deuda Interna con PT",
        xaxis_title="Mes",
        yaxis_title="USD",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig_deuda, use_container_width=True)

# ============================================================================
# TAB 2: PAGOS PT INDIVIDUAL
# ============================================================================

with tab2:
    st.markdown("## 👥 Análisis de Pagos por PT Individual")
    
    st.info("""
    **Esta sección muestra cuánto cobra CADA PT (no el total de los 3).**
    - **Devengado/PT:** Lo que se le "debe" ese mes
    - **Pagado/PT:** Lo que efectivamente cobra
    - **Acumulado/PT:** Total cobrado desde el inicio
    """)
    
    # Selector de escenario
    escenario_sel = st.selectbox(
        "Selecciona un escenario:",
        ['Conservador', 'Base', 'Optimista'],
        index=1
    )
    
    df_sel = resultados[escenario_sel]
    
    # Gráfico Pago Mensual por PT
    fig_pt_pag = go.Figure()
    
    fig_pt_pag.add_trace(go.Scatter(
        x=df_sel['Mes'],
        y=df_sel['PT Pag/PT'],
        name='Pagado/PT',
        line=dict(color='#2E7D32', width=3),
        mode='lines',
        fill='tozeroy'
    ))
    
    fig_pt_pag.add_trace(go.Scatter(
        x=df_sel['Mes'],
        y=df_sel['PT Dev/PT'],
        name='Devengado/PT',
        line=dict(color='#FFA726', width=2, dash='dot'),
        mode='lines'
    ))
    
    # Líneas de referencia
    fig_pt_pag.add_hline(y=1500, line_dash="dash", line_color="blue", 
                          annotation_text="PT@50%: $1,500", annotation_position="right")
    fig_pt_pag.add_hline(y=2250, line_dash="dash", line_color="purple",
                          annotation_text="PT@75%: $2,250", annotation_position="right")
    fig_pt_pag.add_hline(y=3000, line_dash="dash", line_color="red",
                          annotation_text="FT: $3,000", annotation_position="right")
    
    fig_pt_pag.update_layout(
        title=f"Pago Mensual a CADA PT — {escenario_sel}",
        xaxis_title="Mes",
        yaxis_title="USD",
        hovermode='x unified',
        height=450
    )
    
    st.plotly_chart(fig_pt_pag, use_container_width=True)
    
    # Gráfico Acumulado por PT
    fig_pt_acum = go.Figure()
    
    fig_pt_acum.add_trace(go.Scatter(
        x=df_sel['Mes'],
        y=df_sel['PT Acum/PT'],
        name='Acumulado cobrado',
        line=dict(color='#1976D2', width=3),
        mode='lines',
        fill='tozeroy'
    ))
    
    fig_pt_acum.update_layout(
        title=f"Acumulado Cobrado por PT — {escenario_sel}",
        xaxis_title="Mes",
        yaxis_title="USD",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig_pt_acum, use_container_width=True)
    
    # Tabla resumen key months
    st.markdown("### 📋 Resumen de Hitos Clave")
    
    t_full_mes = df_sel[df_sel['T_full Alcanzado']]['Mes'].min() if df_sel['T_full Alcanzado'].any() else None
    t_mid = params['t_mid_base'] if escenario_sel == 'Base' else (18 if escenario_sel == 'Conservador' else 5)
    
    hitos = []
    
    # Mes 1
    mes_1 = df_sel.iloc[0]
    hitos.append({
        'Mes': 1,
        'Hito': 'Inicio',
        'Devengado/PT': f"${mes_1['PT Dev/PT']:,.0f}",
        'Pagado/PT': f"${mes_1['PT Pag/PT']:,.0f}",
        'Acumulado/PT': f"${mes_1['PT Acum/PT']:,.0f}"
    })
    
    # T_mid
    if t_mid <= 36:
        mes_tmid = df_sel[df_sel['Mes'] == t_mid].iloc[0]
        hitos.append({
            'Mes': t_mid,
            'Hito': 'T_mid (PT@50% → PT@75%)',
            'Devengado/PT': f"${mes_tmid['PT Dev/PT']:,.0f}",
            'Pagado/PT': f"${mes_tmid['PT Pag/PT']:,.0f}",
            'Acumulado/PT': f"${mes_tmid['PT Acum/PT']:,.0f}"
        })
    
    # T_full
    if t_full_mes:
        mes_tfull = df_sel[df_sel['Mes'] == t_full_mes].iloc[0]
        hitos.append({
            'Mes': int(t_full_mes),
            'Hito': '🟢 T_full (PT → FT)',
            'Devengado/PT': f"${mes_tfull['PT Dev/PT']:,.0f}",
            'Pagado/PT': f"${mes_tfull['PT Pag/PT']:,.0f}",
            'Acumulado/PT': f"${mes_tfull['PT Acum/PT']:,.0f}"
        })
    
    # Mes 36
    mes_36 = df_sel.iloc[-1]
    hitos.append({
        'Mes': 36,
        'Hito': 'Fin (3 años)',
        'Devengado/PT': f"${mes_36['PT Dev/PT']:,.0f}",
        'Pagado/PT': f"${mes_36['PT Pag/PT']:,.0f}",
        'Acumulado/PT': f"${mes_36['PT Acum/PT']:,.0f}"
    })
    
    st.dataframe(pd.DataFrame(hitos), use_container_width=True, hide_index=True)

# ============================================================================
# TAB 3: ANÁLISIS DE SENSIBILIDAD
# ============================================================================

with tab3:
    st.markdown("## 🎯 Análisis de Sensibilidad al Mix de Cartera")
    
    st.info("Simula automáticamente 4 mix de cartera diferentes y compara su impacto en el escenario Base.")
    
    # Definir 4 mix
    mix_scenarios = {
        'Premium (80% CT3)': {'mix_ct1': 10, 'mix_ct2': 10, 'mix_ct3': 80},
        'Equilibrado (actual)': {'mix_ct1': params['mix_ct1'], 'mix_ct2': params['mix_ct2'], 'mix_ct3': params['mix_ct3']},
        'Diversificado (33% cada)': {'mix_ct1': 33, 'mix_ct2': 34, 'mix_ct3': 33},
        'Entry-Level (80% CT1)': {'mix_ct1': 80, 'mix_ct2': 10, 'mix_ct3': 10},
    }
    
    # Calcular cada mix
    sensibilidad = {}
    for nombre_mix, mix_vals in mix_scenarios.items():
        params_temp = params.copy()
        params_temp.update(mix_vals)
        res_temp, _ = calcular_modelo(params_temp)
        sensibilidad[nombre_mix] = res_temp['Base'].iloc[-1]  # Solo mes 36
    
    # Comparación
    df_sens = pd.DataFrame(sensibilidad).T
    
    st.markdown("### 📊 Comparación de Resultados — Mes 36")
    
    cols_mostrar = ['Saldo Banco', 'PT Acum/PT', 'Revenue Neto', 'Deuda PT']
    df_mostrar = df_sens[cols_mostrar].copy()
    
    # Formatear
    for col in cols_mostrar:
        df_mostrar[col] = df_mostrar[col].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(df_mostrar, use_container_width=True)
    
    # Gráfico de barras comparativo
    fig_sens = go.Figure()
    
    fig_sens.add_trace(go.Bar(
        name='Saldo Banco',
        x=list(sensibilidad.keys()),
        y=[v['Saldo Banco'] for v in sensibilidad.values()],
        marker_color='#70AD47'
    ))
    
    fig_sens.add_trace(go.Bar(
        name='PT Acumulado/PT',
        x=list(sensibilidad.keys()),
        y=[v['PT Acum/PT'] for v in sensibilidad.values()],
        marker_color='#2E7D32'
    ))
    
    fig_sens.update_layout(
        title="Impacto del Mix de Cartera en Saldo y PT",
        xaxis_title="Mix de Cartera",
        yaxis_title="USD",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig_sens, use_container_width=True)

# ============================================================================
# TAB 4: DATOS DETALLADOS
# ============================================================================

with tab4:
    st.markdown("## 📋 Datos Detallados Mes a Mes")
    
    escenario_tabla = st.selectbox(
        "Selecciona escenario para ver tabla completa:",
        ['Conservador', 'Base', 'Optimista'],
        index=1,
        key='tabla_esc'
    )
    
    df_tabla = resultados[escenario_tabla].copy()
    
    # Formatear columnas numéricas
    cols_formato = ['Revenue Neto', 'Cobros', 'Mandatorio', 'PT_pag', 'Deuda PT', 
                    'Saldo Banco', 'PT Pag/PT', 'PT Acum/PT']
    
    for col in cols_formato:
        if col in df_tabla.columns:
            df_tabla[col] = df_tabla[col].apply(lambda x: f"${x:,.0f}")
    
    # Formatear porcentajes
    df_tabla['Utilización'] = df_tabla['Utilización'].apply(lambda x: f"{x*100:.1f}%")
    df_tabla['Dedicación PT'] = df_tabla['Dedicación PT'].apply(lambda x: f"{x*100:.0f}%")
    
    st.dataframe(df_tabla, use_container_width=True, height=600)
    
    # Descarga CSV
    csv = resultados[escenario_tabla].to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Descargar {escenario_tabla} en CSV",
        data=csv,
        file_name=f'quirkosig_{escenario_tabla.lower()}_36m.csv',
        mime='text/csv',
    )

# ============================================================================
# TAB 5: INTERPRETACIÓN
# ============================================================================

with tab5:
    st.markdown("## 📖 Guía de Interpretación")
    
    st.markdown("""
    ### 🎯 Conceptos Clave del Modelo v4
    
    #### 🔄 T_full Dinámico
    - **Antes (v3):** T_full era un mes fijo (ej: mes 15)
    - **Ahora (v4):** T_full se activa cuando **cobros mensuales ≥ USD 18,000**
    - **Ventaja:** Solo te comprometes a pagar 4 FT cuando el revenue lo permite
    
    #### 💰 Evolución del Mandatorio
    
    | Etapa | Mandatorio | Quién cobra |
    |-------|-----------|-------------|
    | **Inicio** | USD 3,000 | 1 FT inicial (USD 2,500 × 1.20 OH) |
    | **Post T_full** | USD 14,400 | 4 FT (USD 3,000 c/u × 1.20 OH) |
    
    #### 👥 Evolución de Pagos a PT
    
    | Mes | Dedicación | Devengado/PT | Cómo cobra |
    |-----|-----------|--------------|-----------|
    | 1 - T_mid | PT@50% | USD 1,500 | Del excedente + margen (modelo diferido) |
    | T_mid - T_full | PT@75% | USD 2,250 | Del excedente + margen (modelo diferido) |
    | Post T_full | FT 100% | USD 3,000 | Del Mandatorio (como cualquier FT) |
    
    ### 📊 Qué Medir en Cada Escenario
    
    #### ✅ Escenario Viable:
    - Saldo banco > USD 0 en mes 36
    - PT acumulado/PT > USD 50,000 al final
    - T_full alcanzado antes del mes 30
    
    #### ⚠️ Señales de Alarma:
    - Saldo banco negativo > USD 20,000
    - T_full nunca se alcanza (revenue < USD 18,000)
    - Deuda PT crece sin control
    
    ### 🔍 Cómo Usar Este Dashboard
    
    1. **Ajusta parámetros** en el sidebar según tu realidad
    2. **Revisa KPIs** en la parte superior — foco en escenario Base
    3. **Analiza Tab "Pagos PT"** para entender cuándo y cuánto cobran
    4. **Valida sensibilidad** al mix de cartera
    5. **Descarga datos** para análisis externo si es necesario
    
    ### 🚀 Decisiones Estratégicas
    
    El modelo te ayuda a responder:
    - **¿Cuándo podemos pasar los 3 PT a FT?** → Cuando cobros >= USD 18,000
    - **¿Qué mix de cartera necesitamos?** → Simula en Tab "Sensibilidad"
    - **¿Es viable con 10% utilización inicial?** → Revisa saldo mes 36
    - **¿Cuánto acumula cada PT en 3 años?** → Ver "PT Acum/PT" mes 36
    
    ### 💡 Tips de Optimización
    
    - **Acelerar T_full:** Aumentar utilización inicial o crecimiento
    - **Maximizar PT acumulado:** Llegar a T_full lo antes posible
    - **Mejorar saldo banco:** Revisar % margen o reducir overhead
    - **Reducir deuda PT:** Aumentar % margen → deuda PT
    """)
    
    st.success("""
    **✨ Este modelo refleja la realidad del negocio:**
    - Los PT no cobran como FT hasta que el revenue lo permite
    - El FT inicial empieza cobrando menos (USD 2,500) hasta normalizar
    - El saldo banco muestra los costos reales (no se infla artificialmente)
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; opacity: 0.7; font-size: 0.9rem;">
    <p>🌿 <strong>QuirkoSIG Dashboard v4.0</strong> | Mayo 2025</p>
    <p>Modelo financiero a 36 meses con T_full dinámico</p>
</div>
""", unsafe_allow_html=True)
