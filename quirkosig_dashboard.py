"""
🌿 QuirkoSIG — Dashboard Financiero Interactivo
Modelo v3.2: Mix de cartera + PT diferidos + 80/20 split

Deploy: streamlit run quirkosig_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ══════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="QuirkoSIG Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1A5C28;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #546E7A;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2E7D32;
    }
    .warning-card {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #D32F2F;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #1565C0;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# SIDEBAR — PARÁMETROS EDITABLES
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚙️ Parámetros del Modelo")
    st.markdown("---")
    
    st.markdown("#### 👥 Equipo")
    N_SENIORS = 4
    N_FT = 1
    FT_SAL = st.number_input("Honorario FT (USD/mes)", value=3000, step=100)
    PT_INI_DED = st.slider("Dedicación PT inicial (%)", 0, 100, 50) / 100
    PT_MID_DED = st.slider("Dedicación PT transición (%)", 0, 100, 75) / 100
    PT_INI_SAL = FT_SAL * PT_INI_DED
    PT_MID_SAL = FT_SAL * PT_MID_DED
    BD_PCT = st.slider("% tiempo no facturable", 0, 50, 20) / 100
    CAP_FT = 1.5 * (1 - BD_PCT)
    
    st.markdown("---")
    st.markdown("#### 💰 Mix de Cartera")
    st.info("Ajustar según la composición típica de proyectos")
    
    REV_CT1 = st.number_input("Revenue CT1 (USD/u/mes)", value=5000, step=500,
                               help="Actividades cortas: cartografía, NDVI, inventarios")
    REV_CT2 = st.number_input("Revenue CT2 (USD/u/mes)", value=10000, step=500,
                               help="Actividades medias: análisis multitemporal, diagnósticos")
    REV_CT3 = st.number_input("Revenue CT3 (USD/u/mes)", value=10000, step=500,
                               help="Actividades complejas: ML, modelos predictivos")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        PCT_CT1 = st.number_input("% CT1", value=20, step=5, min_value=0, max_value=100) / 100
    with col2:
        PCT_CT2 = st.number_input("% CT2", value=60, step=5, min_value=0, max_value=100) / 100
    with col3:
        PCT_CT3 = st.number_input("% CT3", value=20, step=5, min_value=0, max_value=100) / 100
    
    sum_pct = PCT_CT1 + PCT_CT2 + PCT_CT3
    if abs(sum_pct - 1.0) > 0.01:
        st.error(f"⚠️ La suma debe ser 100% (actual: {sum_pct*100:.0f}%)")
    
    BASE_R = REV_CT1 * PCT_CT1 + REV_CT2 * PCT_CT2 + REV_CT3 * PCT_CT3
    st.success(f"⭐ Revenue/u promedio: **USD {BASE_R:,.0f}**/mes")
    
    st.markdown("---")
    st.markdown("#### 📊 Descuentos y Margen")
    MARGIN = st.slider("Margen declarado (%)", 10, 30, 20) / 100
    IIBB = st.slider("IIBB Salta (%)", 0, 5, 3.5) / 100
    INCOB = st.slider("Provisión incobrables (%)", 0, 10, 5) / 100
    TAX = st.slider("Ganancias estimado (%)", 0, 15, 8) / 100
    LAG = st.slider("Lag de cobro (meses)", 1, 3, 2)
    
    PCT_DEBT = st.slider("% margen → deuda PT", 0, 100, 40) / 100
    PCT_INV = 1 - PCT_DEBT
    
    OVH_Y1 = 0.08
    OVH_Y2 = 0.20
    SC_THRESH = N_SENIORS * FT_SAL * (1 + OVH_Y2) / (1 - MARGIN)
    
    st.markdown("---")
    st.info(f"💡 Umbral Sueldo Completo: **USD {SC_THRESH:,.0f}/mes**")

# ══════════════════════════════════════════════════════════════════════
# ESCENARIOS
# ══════════════════════════════════════════════════════════════════════
SCENARIOS = {
    'Conservador': dict(util_ini=0.05, growth=0.040, max_util=0.60,
                        mult=0.80, t_mid=18, t_full=99, anticipo=1500,
                        color='#1565C0'),
    'Base':        dict(util_ini=0.15, growth=0.055, max_util=0.75,
                        mult=1.00, t_mid=8,  t_full=15, anticipo=3000,
                        color='#2E7D32'),
    'Optimista':   dict(util_ini=0.25, growth=0.075, max_util=0.80,
                        mult=1.15, t_mid=5,  t_full=10, anticipo=6000,
                        color='#E65100'),
}
MONTHS = 24

# ══════════════════════════════════════════════════════════════════════
# MOTOR DE CÁLCULO
# ══════════════════════════════════════════════════════════════════════
@st.cache_data
def project_scenario(name, params, _base_r, _ft_sal, _pt_ini_sal, _pt_mid_sal,
                     _bd_pct, _cap_ft, _margin, _iibb, _incob, _tax, _lag,
                     _pct_debt, _pct_inv, _ovh_y1, _ovh_y2):
    """Calcula proyección 24m para un escenario."""
    rows = []
    for m in range(1, MONTHS+1):
        yr = 1 if m <= 12 else 2
        ovh = _ovh_y1 if yr == 1 else _ovh_y2
        
        if m >= params['t_full']: pt_ded = 1.0
        elif m >= params['t_mid']: pt_ded = PT_MID_DED
        else: pt_ded = PT_INI_DED
        
        cap = _cap_ft + 3 * 1.5 * pt_ded * (1 - _bd_pct)
        util = min(params['util_ini'] * (1 + params['growth']) ** (m-1), params['max_util'])
        units = cap * util
        
        dyn_mult = min(0.75 + (params['mult'] - 0.75) * (m/12), params['mult'])
        revenue = units * _base_r * dyn_mult
        
        cost_dev = (_ft_sal + 3 * _ft_sal * pt_ded) * (1 + ovh)
        mg_gross = revenue * (1 - _iibb - _incob) - cost_dev
        mg_net = mg_gross - max(mg_gross * _tax, 0)
        
        rows.append(dict(
            mes=m, año=yr, pt_ded=pt_ded, cap=cap, util=util, units=units,
            revenue=revenue, cost_dev=cost_dev,
            mg_gross=mg_gross, mg_net=mg_net,
        ))
    df = pd.DataFrame(rows)
    
    # Flujo de caja
    df['cobros'] = 0.0
    df.loc[df.mes == 1, 'cobros'] = params['anticipo']
    for m in range(3, MONTHS+1):
        if m > _lag:
            df.loc[df.mes == m, 'cobros'] = df.loc[df.mes == m - _lag, 'revenue'].values[0]
    
    df['c80'] = df['cobros'] * 0.80
    df['mandatorio'] = df.apply(
        lambda r: _ft_sal * (1 + (_ovh_y1 if r['año'] == 1 else _ovh_y2)), axis=1)
    df['excedente'] = (df['c80'] - df['mandatorio']).clip(lower=0)
    df['margen'] = df['cobros'] * _margin
    
    def pt_dev_month(r):
        if r['mes'] >= params['t_full']: return 0
        if r['mes'] >= params['t_mid']: return 3 * _pt_mid_sal
        return 3 * _pt_ini_sal
    df['pt_dev'] = df.apply(pt_dev_month, axis=1)
    
    # Iterativo para deuda
    pt_paid = []; deuda = []; mg_a_deuda = []
    fondo_inv = []; fondo_inv_acum = []; saldo_banco = []
    deu_prev = 0; saldo_prev = 0; inv_acum_prev = 0
    
    for _, r in df.iterrows():
        mgd = r['margen'] * _pct_debt if (deu_prev > 0 or (r['mes'] == 1 and r['pt_dev'] > 0)) else 0
        deuda_total = r['pt_dev'] + deu_prev
        ptp = min(r['excedente'] + mgd, deuda_total)
        deu_new = deu_prev + r['pt_dev'] - ptp
        finv = r['margen'] if deu_new == 0 else r['margen'] * _pct_inv
        sb = saldo_prev + r['cobros'] - r['mandatorio'] - ptp
        inv_acum = inv_acum_prev + finv
        
        mg_a_deuda.append(mgd); pt_paid.append(ptp); deuda.append(deu_new)
        fondo_inv.append(finv); fondo_inv_acum.append(inv_acum); saldo_banco.append(sb)
        deu_prev = deu_new; saldo_prev = sb; inv_acum_prev = inv_acum
    
    df['mg_a_deuda'] = mg_a_deuda
    df['pt_pagado'] = pt_paid
    df['deuda_pt'] = deuda
    df['fondo_inv'] = fondo_inv
    df['fondo_acum'] = fondo_inv_acum
    df['saldo_banco'] = saldo_banco
    
    df['pt_pagado_individual'] = df['pt_pagado'] / 3
    df['pt_devengado_individual'] = df['pt_dev'] / 3
    df['pt_acum_individual'] = df['pt_pagado_individual'].cumsum()
    df['escenario'] = name
    
    return df

# Calcular escenarios
results = {n: project_scenario(n, p, BASE_R, FT_SAL, PT_INI_SAL, PT_MID_SAL,
                                BD_PCT, CAP_FT, MARGIN, IIBB, INCOB, TAX, LAG,
                                PCT_DEBT, PCT_INV, OVH_Y1, OVH_Y2)
           for n, p in SCENARIOS.items()}

# ══════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="main-header">🌿 QuirkoSIG — Dashboard Financiero</div>', 
            unsafe_allow_html=True)
st.markdown('<div class="sub-header">Proyecciones financieras 24 meses · Mix de cartera + PT diferidos</div>', 
            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# KPIs PRINCIPALES
# ══════════════════════════════════════════════════════════════════════
st.markdown("### 📊 KPIs por Escenario")

cols = st.columns(3)
for i, (name, df) in enumerate(results.items()):
    with cols[i]:
        color = SCENARIOS[name]['color']
        deficit = abs(min(df.saldo_banco.min(), 0))
        cobrado_pt = df.pt_acum_individual.iloc[-1]
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {color}22 0%, {color}44 100%); 
                    padding: 1.5rem; border-radius: 10px; border-left: 4px solid {color};'>
            <h3 style='color: {color}; margin: 0;'>{name}</h3>
            <div style='margin-top: 1rem;'>
                <p style='margin: 0.5rem 0;'><strong>Revenue 24m:</strong> USD {df.revenue.sum():,.0f}</p>
                <p style='margin: 0.5rem 0;'><strong>Déficit banco máx:</strong> USD {deficit:,.0f}</p>
                <p style='margin: 0.5rem 0;'><strong>Deuda PT máx:</strong> USD {df.deuda_pt.max():,.0f}</p>
                <p style='margin: 0.5rem 0; font-size: 1.1rem; color: {color};'>
                    <strong>💰 Cobrado por c/PT:</strong> USD {cobrado_pt:,.0f}
                </p>
                <p style='margin: 0.5rem 0; font-size: 0.9rem; color: #666;'>
                    Promedio: USD {cobrado_pt/24:,.0f}/mes
                </p>
                <p style='margin: 0.5rem 0;'><strong>Fondo inversión:</strong> USD {df.fondo_acum.iloc[-1]:,.0f}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TABS DE NAVEGACIÓN
# ══════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Revenue & Flujo", 
    "👥 Pagos PT Individuales", 
    "🎯 Análisis de Sensibilidad",
    "📋 Datos Detallados",
    "📖 Interpretación"
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1: REVENUE & FLUJO
# ══════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 💰 Revenue Mensual")
    
    fig1 = go.Figure()
    for name, df in results.items():
        fig1.add_trace(go.Scatter(
            x=df.mes, y=df.revenue, name=name,
            line=dict(color=SCENARIOS[name]['color'], width=3),
            mode='lines+markers'
        ))
    
    fig1.add_hline(y=SC_THRESH, line=dict(color='gold', width=2, dash='dash'),
                   annotation_text=f'Umbral SC: USD {SC_THRESH:,.0f}')
    
    fig1.update_layout(
        height=450, template='plotly_white',
        xaxis_title='Mes', yaxis_title='Revenue mensual (USD)',
        hovermode='x unified', legend=dict(orientation='h', y=1.1)
    )
    fig1.update_yaxes(tickformat=',.0f')
    st.plotly_chart(fig1, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ⚠️ Saldo Bancario Real")
        fig2 = go.Figure()
        for name, df in results.items():
            fig2.add_trace(go.Scatter(
                x=df.mes, y=df.saldo_banco, name=name,
                line=dict(color=SCENARIOS[name]['color'], width=3)
            ))
        fig2.add_hline(y=0, line=dict(color='red', width=1, dash='dot'))
        fig2.update_layout(
            height=400, template='plotly_white',
            xaxis_title='Mes', yaxis_title='Saldo banco (USD)',
            hovermode='x unified', showlegend=False
        )
        fig2.update_yaxes(tickformat=',.0f')
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("### 🔴 Deuda Interna con PT")
        fig3 = go.Figure()
        for name, df in results.items():
            fig3.add_trace(go.Scatter(
                x=df.mes, y=df.deuda_pt, name=name,
                line=dict(color=SCENARIOS[name]['color'], width=3)
            ))
        fig3.update_layout(
            height=400, template='plotly_white',
            xaxis_title='Mes', yaxis_title='Deuda PT (USD)',
            hovermode='x unified', showlegend=False
        )
        fig3.update_yaxes(tickformat=',.0f')
        st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 2: PAGOS PT INDIVIDUALES
# ══════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 👥 Lo que cobra CADA PT mes a mes")
    st.info("💡 El PT pagado total se distribuye en partes iguales entre los 3 PT")
    
    fig4 = go.Figure()
    for name, df in results.items():
        fig4.add_trace(go.Scatter(
            x=df.mes, y=df.pt_pagado_individual, name=name,
            line=dict(color=SCENARIOS[name]['color'], width=3),
            mode='lines+markers'
        ))
    
    fig4.add_hline(y=PT_INI_SAL, line=dict(color='gray', width=1, dash='dash'),
                   annotation_text=f'USD {PT_INI_SAL:,.0f} (PT 50%)')
    fig4.add_hline(y=FT_SAL, line=dict(color='red', width=2, dash='dash'),
                   annotation_text=f'USD {FT_SAL:,.0f} (FT completo)')
    
    fig4.update_layout(
        height=450, template='plotly_white',
        xaxis_title='Mes', yaxis_title='Pago mensual por PT (USD)',
        hovermode='x unified', legend=dict(orientation='h', y=1.1)
    )
    fig4.update_yaxes(tickformat=',.0f')
    st.plotly_chart(fig4, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 Acumulado cobrado por cada PT")
        fig5 = go.Figure()
        for name, df in results.items():
            fig5.add_trace(go.Scatter(
                x=df.mes, y=df.pt_acum_individual, name=name,
                line=dict(color=SCENARIOS[name]['color'], width=3),
                fill='tonexty' if name != 'Conservador' else None
            ))
        fig5.update_layout(
            height=400, template='plotly_white',
            xaxis_title='Mes', yaxis_title='Total acumulado por PT (USD)',
            hovermode='x unified', showlegend=False
        )
        fig5.update_yaxes(tickformat=',.0f')
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        st.markdown("### ⚖️ Devengado vs Pagado (Base)")
        df_base = results['Base']
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(
            x=df_base.mes, y=df_base.pt_devengado_individual,
            name='Devengado/PT', marker_color='#FFC107'
        ))
        fig6.add_trace(go.Bar(
            x=df_base.mes, y=df_base.pt_pagado_individual,
            name='Pagado/PT', marker_color='#2E7D32'
        ))
        fig6.update_layout(
            height=400, template='plotly_white', barmode='overlay',
            xaxis_title='Mes', yaxis_title='USD/mes',
            hovermode='x unified', legend=dict(orientation='h', y=1.1)
        )
        fig6.update_yaxes(tickformat=',.0f')
        st.plotly_chart(fig6, use_container_width=True)
    
    # Tabla resumen PT
    st.markdown("### 📋 Resumen de pagos por PT")
    summary_pt = []
    for name, df in results.items():
        mes_deuda_cero = df[df.deuda_pt == 0].mes.iloc[0] if (df.deuda_pt == 0).any() else 'No en 24m'
        primer_pago_1500 = df[df.pt_pagado_individual > 1500].mes.iloc[0] if (df.pt_pagado_individual > 1500).any() else 'No en 24m'
        primer_pago_3000 = df[df.pt_pagado_individual >= 3000].mes.iloc[0] if (df.pt_pagado_individual >= 3000).any() else 'No en 24m'
        
        summary_pt.append({
            'Escenario': name,
            'Total cobrado por PT': f'USD {df.pt_acum_individual.iloc[-1]:,.0f}',
            'Promedio mensual': f'USD {df.pt_acum_individual.iloc[-1]/24:,.0f}',
            'Mes deuda = 0': str(mes_deuda_cero),
            '1er mes > USD 1.500': str(primer_pago_1500),
            '1er mes = USD 3.000': str(primer_pago_3000),
        })
    
    st.dataframe(pd.DataFrame(summary_pt).set_index('Escenario'), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 3: SENSIBILIDAD
# ══════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 🎯 Análisis de Sensibilidad al Mix de Cartera")
    st.info("¿Qué pasa si la cartera tiene más CT3 (premium) o más CT1 (proyectos pequeños)?")
    
    MIX_VARIANTS = {
        'Mix Estándar (20/60/20)':   {'CT1': 0.20, 'CT2': 0.60, 'CT3': 0.20},
        'Mix Premium (10/50/40)':    {'CT1': 0.10, 'CT2': 0.50, 'CT3': 0.40},
        'Mix Conservador (40/55/5)': {'CT1': 0.40, 'CT2': 0.55, 'CT3': 0.05},
        'Mix CT2 puro (0/100/0)':    {'CT1': 0.00, 'CT2': 1.00, 'CT3': 0.00},
    }
    
    fig_sens = go.Figure()
    colors_mix = ['#1565C0', '#E65100', '#558B2F', '#6A1B9A']
    
    for i, (label, mix) in enumerate(MIX_VARIANTS.items()):
        base_r_var = REV_CT1 * mix['CT1'] + REV_CT2 * mix['CT2'] + REV_CT3 * mix['CT3']
        df_temp = project_scenario('Base', SCENARIOS['Base'], base_r_var, FT_SAL,
                                    PT_INI_SAL, PT_MID_SAL, BD_PCT, CAP_FT,
                                    MARGIN, IIBB, INCOB, TAX, LAG,
                                    PCT_DEBT, PCT_INV, OVH_Y1, OVH_Y2)
        fig_sens.add_trace(go.Scatter(
            x=df_temp.mes, y=df_temp.revenue,
            name=f'{label}<br>USD {base_r_var:,.0f}/u',
            line=dict(color=colors_mix[i], width=3)
        ))
    
    fig_sens.add_hline(y=SC_THRESH, line=dict(color='gold', width=2, dash='dash'),
                       annotation_text=f'Umbral SC: USD {SC_THRESH:,.0f}')
    
    fig_sens.update_layout(
        height=500, template='plotly_white',
        xaxis_title='Mes', yaxis_title='Revenue mensual (USD)',
        hovermode='x unified', legend=dict(orientation='v', x=1.02, y=1)
    )
    fig_sens.update_yaxes(tickformat=',.0f')
    st.plotly_chart(fig_sens, use_container_width=True)
    
    st.markdown("#### 📊 Impacto en KPIs (escenario Base)")
    sensitivity_data = []
    for label, mix in MIX_VARIANTS.items():
        base_r_var = REV_CT1 * mix['CT1'] + REV_CT2 * mix['CT2'] + REV_CT3 * mix['CT3']
        df_temp = project_scenario('Base', SCENARIOS['Base'], base_r_var, FT_SAL,
                                    PT_INI_SAL, PT_MID_SAL, BD_PCT, CAP_FT,
                                    MARGIN, IIBB, INCOB, TAX, LAG,
                                    PCT_DEBT, PCT_INV, OVH_Y1, OVH_Y2)
        sensitivity_data.append({
            'Mix': label,
            'Revenue/u': f'USD {base_r_var:,.0f}',
            'Revenue 24m': f'USD {df_temp.revenue.sum():,.0f}',
            'Cobrado por PT': f'USD {df_temp.pt_acum_individual.iloc[-1]:,.0f}',
            'Fondo Inversión': f'USD {df_temp.fondo_acum.iloc[-1]:,.0f}',
        })
    st.dataframe(pd.DataFrame(sensitivity_data).set_index('Mix'), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 4: DATOS DETALLADOS
# ══════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 📋 Datos Mes a Mes")
    
    escenario_sel = st.selectbox("Seleccionar escenario", list(results.keys()))
    df_sel = results[escenario_sel]
    
    # Tabla completa
    cols_show = ['mes', 'revenue', 'cobros', 'mandatorio', 'pt_dev', 'pt_pagado',
                 'pt_pagado_individual', 'deuda_pt', 'saldo_banco', 'fondo_acum']
    df_display = df_sel[cols_show].copy()
    df_display.columns = ['Mes', 'Revenue', 'Cobros', 'Mandatorio', 'PT dev. total',
                          'PT pag. total', 'PT pag/persona', 'Deuda PT', 'Saldo banco', 'Fondo Inv.']
    
    # Formatear columnas numéricas
    for c in df_display.columns[1:]:
        df_display[c] = df_display[c].apply(lambda v: f'USD {v:,.0f}')
    
    st.dataframe(df_display, use_container_width=True, height=600)
    
    # Botón de descarga
    csv = df_sel.to_csv(index=False)
    st.download_button(
        label=f"📥 Descargar {escenario_sel} en CSV",
        data=csv,
        file_name=f'quirkosig_{escenario_sel.lower()}.csv',
        mime='text/csv'
    )

# ══════════════════════════════════════════════════════════════════════
# TAB 5: INTERPRETACIÓN
# ══════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("### 📖 Cómo interpretar los resultados")
    
    st.markdown("""
    <div class="info-box">
    <h4>💰 Cobrado por cada PT</h4>
    <p>Es el <strong>dato más importante para los socios PT</strong>. Es la suma de todo lo que cada uno recibe 
    desde el mes 1 hasta el mes 24.</p>
    <p>En el escenario Base, USD 26.250 ÷ 24 meses = USD 1.094/mes promedio. Pero este promedio es engañoso:</p>
    <ul>
        <li>Los primeros meses los PT cobran poco (o nada)</li>
        <li>A partir del mes 15 (T_full) cobran USD 3.000/mes completo</li>
        <li>La hoja <strong>PT INDIVIDUAL</strong> del Excel muestra la trayectoria real mes a mes</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <h4>⚠️ Déficit bancario máximo</h4>
    <p>Es el <strong>efectivo real que se necesita</strong> antes de lanzar para no quedarse sin dinero.</p>
    <p>En el Base son USD 4.216 — equivale a menos de 2 semanas del salario del FT. 
    Se puede cubrir con ahorros personales o el anticipo del primer cliente.</p>
    <p><strong>Esto NO es lo mismo que la deuda interna con PT</strong>, que es un compromiso entre socios 
    que se cancela cuando el negocio genera margen.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <h4>🔴 Deuda interna con PT</h4>
    <p>Lo que la empresa les debe a los socios PT por trabajo ya entregado pero no cobrado.</p>
    <p>En el Base llega a USD 55.638 en el peor momento (mes 13), que son ~USD 18.500 por PT.</p>
    <p><strong>No es deuda bancaria</strong> — no genera intereses, no es urgente. 
    Es un crédito interno entre socios que se cancela cuando hay revenue suficiente.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✅ Recomendaciones")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-card">
        <h4>Para arrancar (Base)</h4>
        <ul>
            <li>2 proyectos comprometidos al lanzar</li>
            <li>USD 4.000 de buffer personal</li>
            <li>Pipeline con 2-3 oportunidades calificadas</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-card">
        <h4>Señales de alarma</h4>
        <ul>
            <li>Mes 6 sin 2 proyectos activos → activar plan comercial</li>
            <li>Revenue real < 70% del Base por 2 meses → revisar estrategia</li>
            <li>Deuda PT > USD 60.000 sin tender a bajar → renegociar</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>QuirkoSIG — Dashboard Financiero v3.2 · 2025</p>
    <p>Modelo: Mix de cartera + PT diferidos + 80/20 split</p>
    <p>💡 Tip: Ajustar parámetros en el sidebar y ver el impacto en tiempo real</p>
</div>
""", unsafe_allow_html=True)
