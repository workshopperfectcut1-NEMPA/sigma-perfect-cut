import streamlit as st
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
from shapely.affinity import rotate, translate
import numpy as np
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Perfect Cut", layout="wide")

# CSS AJUSTADO
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2.5rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

# --- TÍTULO ---
st.markdown("## 🔪 The Perfect Cut Challenge <small>(Human vs. Machine)</small>", unsafe_allow_html=True)

# --- ESTADO (SESSION STATE) ---
if 'mostrou_resultado' not in st.session_state:
    st.session_state.mostrou_resultado = False

def resetar_resultado():
    st.session_state.mostrou_resultado = False

# --- MOTOR GEOMÉTRICO ---
coords_brownie = [(-2, -2), (1, -3), (3, 0), (2, 3), (-3, 2)]
brownie = Polygon(coords_brownie)
area_total = brownie.area

# --- LAYOUT PRINCIPAL ---
col_esq, col_dir = st.columns([1, 2], gap="large")

# COLUNA DA ESQUERDA (CONTROLES)
with col_esq:
    st.info("🎛️ **Control Panel**")
    
    # Sliders
    angulo = st.slider("1. Knife Angle (°)", 0, 180, 0, on_change=resetar_resultado)
    posicao = st.slider("2. Knife Position", -4.0, 4.0, 0.0, step=0.05, on_change=resetar_resultado)
    
    st.write("") 
    
    # Botão de Submissão Manual (Atualizado para nova sintaxe)
    # Trocamos use_container_width=True por width='stretch' conforme o aviso
    if st.button("🚀 SUBMIT CUT", width='stretch', type="primary"):
        st.session_state.mostrou_resultado = True
    
    st.divider()
    
    # Busca Binária
    with st.expander("🕵️ Ask the Algorithm"):
        if st.button("RUN BINARY SEARCH"):
            st.session_state.mostrou_resultado = False
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            min_pos, max_pos = -4.0, 4.0
            
            # Loop visual da busca
            for i in range(20):
                mid_pos = (min_pos + max_pos) / 2
                f_temp = rotate(translate(Polygon([(-10,-10),(-10,10),(0,10),(0,-10)]), xoff=mid_pos), angulo, origin=(0,0))
                
                if brownie.intersection(f_temp).area < area_total/2:
                    min_pos = mid_pos
                else:
                    max_pos = mid_pos
                
                progress_bar.progress((i+1)*5)
                time.sleep(0.02)
            
            st.success(f"Optimal Position: { (min_pos+max_pos)/2 :.5f}")

# CÁLCULOS
faca = rotate(translate(Polygon([(-10,-10),(-10,10),(0,10),(0,-10)]), xoff=posicao), angulo, origin=(0,0))
pedaco = brownie.intersection(faca)
area_corte = pedaco.area
erro = ((area_corte - (area_total/2)) / (area_total/2)) * 100

# COLUNA DA DIREITA (VISUALIZAÇÃO)
with col_dir:
    sub_col_plot, sub_col_metrics = st.columns([2, 1])
    
    with sub_col_plot:
        fig, ax = plt.subplots(figsize=(5, 5))
        x, y = brownie.exterior.xy
        ax.fill(x, y, alpha=0.5, fc='gray', ec='black', lw=2)
        
        # Linha Visual
        rad = np.radians(angulo)
        lx, ly = rotate(LineString([(posicao, -10), (posicao, 10)]), angulo, origin=(0,0)).xy
        ax.plot(lx, ly, color='#FF4B4B', lw=3, ls='--')

        if not pedaco.is_empty:
             geoms = [pedaco] if pedaco.geom_type == 'Polygon' else pedaco.geoms
             for p in geoms:
                 xp, yp = p.exterior.xy
                 ax.fill(xp, yp, alpha=0.6, fc='#4488ff', hatch='//')

        ax.set_xlim(-5, 5); ax.set_ylim(-5, 5); ax.axis('off')
        # Atualizado para nova sintaxe aqui também
        st.pyplot(fig, width='stretch')

    with sub_col_metrics:
        st.markdown("### Results")
        if st.session_state.mostrou_resultado:
            st.metric("Total Area", f"{area_total:.2f}")
            st.metric("Your Cut", f"{area_corte:.2f}")
            
            if abs(erro) < 1.0:
                st.metric("Error", f"{erro:.2f}%", delta="PERFECT!")
                st.balloons()
            else:
                st.metric("Error", f"{erro:.2f}%", delta="Fail", delta_color="inverse")
        else:
            st.info("Adjust sliders & click SUBMIT.")
 # --- SIDEBAR (Contador e Créditos) ---
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🌍 Visitor Tracker")
    
    # Substitua o código abaixo pelo que você copiou do site Flag Counter
    # Importante: Mantenha o unsafe_allow_html=True
    st.markdown("""
    <a href="https://info.flagcounter.com/50Hp"><img src="https://s01.flagcounter.com/count2/50Hp/bg_FFFFFF/txt_000000/border_CCCCCC/columns_2/maxflags_10/viewers_0/labels_0/pageviews_0/flags_0/percent_0/" alt="Flag Counter" border="0"></a>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**Developed by:** Prof. Roberto Sant'Anna")
    st.markdown("© 2026 NEMPA - UFBA")