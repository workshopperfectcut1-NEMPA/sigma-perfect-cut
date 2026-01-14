import streamlit as st
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from shapely.affinity import rotate
import random
import numpy as np
import time

# Import functions from utils module
from utils import (
    create_brownie,
    create_complex_polygon,
    calculate_cut,
    calculate_error,
    optimized_binary_search,
    emoji_rain
)

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Perfect Cut", layout="wide")

# ADJUSTED CSS
st.markdown("""
    <style>
        .block-container {
            padding-top: 2.5rem;
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.markdown("## 🔪 The Perfect Cut Challenge <small>(Human vs. Machine)</small>", unsafe_allow_html=True)

# --- STATE (SESSION STATE) ---
if "showed_result" not in st.session_state:
    st.session_state.showed_result = False
if "search_history" not in st.session_state:
    st.session_state.search_history = None

def reset_result():
    st.session_state.showed_result = False
    st.session_state.search_history = None

# --- GEOMETRIC ENGINE ---
brownie = create_brownie()
total_area = brownie.area

if "brownie" not in st.session_state:
    st.session_state.brownie = brownie
if "total_area" not in st.session_state:
    st.session_state.total_area = total_area

brownie = st.session_state.brownie
total_area = st.session_state.total_area

# --- MAIN LAYOUT ---
col_left, col_right = st.columns([1, 2], gap="large")


def chaos_mode_changed():
    print("chaos mode changed:", chaos_mode)    
    reset_result()
    # Caso esteja no chaos mode...
    if not chaos_mode:
        st.session_state.brownie = create_complex_polygon()
        st.session_state.random_angle = random.uniform(-180.0, 0.0)
        
        
    # Caso NÃO esteja no chaos mode...
    else:
        st.session_state.brownie = create_brownie()
    st.session_state.total_area = st.session_state.brownie.area


# LEFT COLUMN (CONTROLS)
with col_left:
    st.info("🎛️ **Control Panel**")
    
    # Sliders
    chaos_mode = st.checkbox("🔥 Clara", value=False, on_change=chaos_mode_changed)
    if chaos_mode:
        angle = st.slider("1. Knife Angle (°)", -180.0, 0.0, st.session_state.random_angle, step=0.1, on_change=reset_result)
        angle = abs(angle)
        print("angle selected:", angle)
        position = st.slider("2. Knife Position", -4.0, 4.0, -4.0, step=0.05, on_change=reset_result)
    else:
        angle = st.slider("1. Knife Angle (°)", 0, 180, 0, on_change=reset_result)
        position = st.slider("2. Knife Position", -4.0, 4.0, 0.0, step=0.05, on_change=reset_result)
    
    st.write("") 
    
    # Manual Submission Button
    if st.button("🚀 SUBMIT CUT", width="content", type="primary"):
        st.session_state.showed_result = True
    
    st.divider()
    
    # Binary Search
    with st.expander("🕵️ Ask the Algorithm", expanded=False):
        num_iterations = st.number_input(
            "Number of iterations",
            min_value=5,
            max_value=50,
            value=20,
            step=1,
            help="More iterations = higher precision"
        )
        
        if st.button("RUN BINARY SEARCH", width="content"):
            st.session_state.showed_result = False
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Execute binary search
            result = optimized_binary_search(
                brownie, 
                angle, 
                num_iterations=num_iterations
            )
            
            # Visual progress animation
            for i in range(num_iterations):
                progress_bar.progress((i + 1) / num_iterations)
                status_text.text(f"Iteration {i+1}/{num_iterations}: Error = {result['error_history'][i]:.3f}%")
                time.sleep(0.05)
            
            st.session_state.search_history = result
            
            st.success(f"✅ Optimal Position: {result['optimal_position']:.5f}")
            st.info(f"📊 Final Error: {result['error_history'][-1]:.5f}%")

# CALCULATIONS
piece, cut_area = calculate_cut(brownie, position, angle)
error = calculate_error(cut_area, total_area)

# RIGHT COLUMN (VISUALIZATION)
with col_right:
    sub_col_plot, sub_col_metrics = st.columns([2, 1])
    
    with sub_col_plot:
        # Fixed aspect ratio and responsive sizing
        fig, ax = plt.subplots(figsize=(6, 6))
        x, y = brownie.exterior.xy
        ax.fill(x, y, alpha=0.5, fc="gray", ec="black", lw=2)
        
        # Visual Line
        rad = np.radians(angle)
        lx, ly = rotate(LineString([(position, -10), (position, 10)]), angle, origin=(0, 0)).xy
        ax.plot(lx, ly, color="#FF4B4B", lw=3, ls="--")

        if not piece.is_empty:
            geoms = [piece] if piece.geom_type == "Polygon" else piece.geoms
            for p in geoms:
                xp, yp = p.exterior.xy
                ax.fill(xp, yp, alpha=0.6, fc="#4488ff", hatch="//")

        # Fixed limits and aspect ratio
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_aspect("equal", adjustable="box")
        ax.axis("off")
        
        # Use container width for responsiveness
        st.pyplot(fig, width="content")
        plt.close(fig)

with sub_col_metrics:
        st.markdown("### Results")
        if st.session_state.showed_result:
            st.metric("Total Area", f"{total_area:.2f}")
            st.metric("Your Cut", f"{cut_area:.2f}")
            st.metric("Error", f"{error:.2f}%")
            
            abs_error = abs(error)
            
            if abs_error < 1.0:
                st.success("🎯 **PERFECT CUT!** 🎉")
                st.balloons()
                
            elif abs_error < 2.0:
                st.success("✨ **Super!** Great job! 👏")
                emoji_rain("👏") 
                
            elif abs_error < 5.0:
                st.info("👍 **Good attempt!** Keep refining!")
                emoji_rain("👍") 
                
            elif abs_error < 10.0:
                st.warning("⚠️ **Unbalanced Split** - Try again!")
                emoji_rain("⚠️")
                
            else:
                st.error("😠 **Very Unbalanced!** 💢")
                st.markdown("**Tip:** Use the Binary Search for guidance!")
                emoji_rain("💢") 

# --- BINARY SEARCH CONVERGENCE GRAPHS ---
if st.session_state.search_history is not None:
    st.divider()
    st.markdown("### 📈 Binary Search Convergence")
    
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        # Error Graph with fixed aspect
        fig_error, ax_error = plt.subplots(figsize=(7, 5))
        iterations = list(range(1, len(st.session_state.search_history["error_history"]) + 1))
        ax_error.plot(iterations, st.session_state.search_history["error_history"], 
                     marker="o", color="#FF4B4B", linewidth=2, markersize=4)
        ax_error.axhline(y=0, color="green", linestyle="--", alpha=0.5, label="Perfect Cut")
        ax_error.set_xlabel("Iteration", fontsize=11)
        ax_error.set_ylabel("Error (%)", fontsize=11)
        ax_error.set_title("Error Convergence", fontsize=12, fontweight="bold", pad=15)
        ax_error.grid(True, alpha=0.3)
        ax_error.legend()
        fig_error.tight_layout()
        st.pyplot(fig_error, width="content")
        plt.close(fig_error)
    
    with col_graph2:
        # Position Graph with fixed aspect
        fig_pos, ax_pos = plt.subplots(figsize=(7, 5))
        ax_pos.plot(iterations, st.session_state.search_history["position_history"], 
                    marker="s", color="#4488ff", linewidth=2, markersize=4)
        ax_pos.axhline(y=st.session_state.search_history["optimal_position"], 
                       color="green", linestyle="--", alpha=0.5, label="Optimal Position")
        ax_pos.set_xlabel("Iteration", fontsize=11)
        ax_pos.set_ylabel("Position", fontsize=11)
        ax_pos.set_title("Position Convergence", fontsize=12, fontweight="bold", pad=15)
        ax_pos.grid(True, alpha=0.3)
        ax_pos.legend()
        fig_pos.tight_layout()
        st.pyplot(fig_pos, width="content")
        plt.close(fig_pos)

# --- SIDEBAR (Counter and Credits) ---
with st.sidebar:
    st.divider()
    
    st.markdown("### 🏆 The Team (NEMPA)")
    
    # Project Lead
    st.markdown("**Project Lead**")
    st.markdown("👨‍🏫 *Prof. Dr. Roberto Sant'Anna*")
    
    st.write("") # Espaço para separar
    
    # Lead Dev
    st.markdown("**Lead Developer**")
    st.markdown("🛠️ *Enzo Ribeiro*")
    
    st.write("")
    
    # Core Dev (Reconhecimento técnico)
    st.markdown("**Core Developer**")
    st.markdown("🧠 *Ikaro Vieira*")
    
    st.write("")

    # Scientific Devs (O time de apoio)
    st.markdown("**Scientific Developers**")
    st.markdown("💻 *Felipe Brasileiro*")
    st.markdown("💻 *Iago Nunes*")

    st.divider()
    
    # Visitor Counter (Mantivemos o código do contador)
    st.markdown("### 🌍 Visitor Tracker")
    st.markdown("""
         <a href="https://info.flagcounter.com/50Hp">
                <img src="https://s01.flagcounter.com/count2/50Hp/bg_FFFFFF/txt_000000/border_CCCCCC/columns_2/maxflags_10/viewers_0/labels_0/pageviews_0/flags_0/percent_0/" 
                alt="Flag Counter" border="0">
                </a>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("© 2026 NEMPA - UFBA")
