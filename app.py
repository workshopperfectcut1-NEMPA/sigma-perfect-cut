import streamlit as st
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from shapely.affinity import rotate
import random
import numpy as np
import time
from streamlit_local_storage import LocalStorage

# Import functions from utils module
from utils import (
    create_brownie,
    create_complex_polygon,
    calculate_cut,
    calculate_error,
    optimized_binary_search,
    emoji_rain
)

# Filenames kept as original to prevent FileNotFoundError
audio_file = open("vitória  🔊 efeito sonoro para vídeo🔊 - Efeitos sonoros (youtube).mp3", "rb")
audio_bytes = audio_file.read()
audio_file_lose = open("perca.mp3", "rb")
audio_bytes_lose = audio_file_lose.read()

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Perfect Cut", layout="wide")
localS = LocalStorage()

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
        audio {
            visibility: hidden;
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
    # If in chaos mode...
    if not chaos_mode:
        st.session_state.brownie = create_complex_polygon()
        st.session_state.random_angle = random.uniform(-180.0, 0.0)
        
        
    # If NOT in chaos mode...
    else:
        st.session_state.brownie = create_brownie()
    st.session_state.total_area = st.session_state.brownie.area


# --- LEFT COLUMN (CONTROLS) ---
with col_left:
    st.info("🎛️ **Control Panel**")
    
    with st.container(border=True):
        # 1. Chaos Mode Checkbox
        chaos_mode = st.checkbox("🔥 Chaos Mode", value=False, on_change=chaos_mode_changed)
        
        st.divider()

        # 2. AI Auto-Lock (The feature you asked for)
        # This forces the knife to always seek the 50/50 cut based on the angle
        ai_lock = st.toggle("🤖 AI Auto-Lock (Follow Perfect Cut)", value=False, help="Automatically adjusts position to maintain 50% area as you rotate.")
        
        st.write("")

        # 3. Angle Slider
        # Determine ranges based on Chaos Mode
        if chaos_mode:
            min_ang, max_ang = -180.0, 0.0
            def_ang = st.session_state.random_angle
        else:
            min_ang, max_ang = 0.0, 180.0
            def_ang = 0.0
            
        angle = st.slider(
            "1. Knife Angle (°)", 
            min_value=float(min_ang), 
            max_value=float(max_ang), 
            value=float(def_ang), 
            step=0.5, 
            on_change=reset_result
        )

        # 4. Position Slider Logic
        # We define min/max for position
        min_pos, max_pos = -4.0, 4.0
        
        if ai_lock:
            # --- REAL-TIME AI CALCULATION ---
            # Run a fast binary search (10 iterations is enough for smooth UI)
            # to find the perfect position for the CURRENT angle.
            fast_search = optimized_binary_search(st.session_state.brownie, angle, num_iterations=10)
            optimal_pos = fast_search['optimal_position']
            
            # Clip to slider limits to prevent errors
            optimal_pos = np.clip(optimal_pos, min_pos, max_pos)
            
            # Update 'position' variable
            position = optimal_pos
            
            # Display DISABLED slider but with UPDATED value
            st.slider("2. Knife Position (Auto)", min_pos, max_pos, value=float(position), disabled=True)
            st.caption(f"🤖 AI Target: **{position:.4f}**")
            
        else:
            # Manual Mode
            position = st.slider(
                "2. Knife Position", 
                min_pos, max_pos, 
                value=0.0, 
                step=0.05, 
                on_change=reset_result
            )

    st.write("") 
    
    # Manual Submission Button
    if st.button("🚀 SUBMIT CUT", width="content", type="primary"):
        st.session_state.showed_result = True        
    
    st.divider()
    
    # Detailed Binary Search (The educational part)
    with st.expander("🕵️ Ask the Algorithm (Step-by-Step)", expanded=False):
        num_iterations = st.number_input(
            "Number of iterations",
            min_value=5, max_value=50, value=20, step=1,
            help="More iterations = higher precision"
        )
        
        if st.button("RUN BINARY SEARCH", width="content"):
            st.session_state.showed_result = False
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Execute binary search
            result = optimized_binary_search(st.session_state.brownie, angle, num_iterations=num_iterations)
            
            # Animation
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
            name = st.text_input("Enter your name for the ranking:", max_chars=20)
            if st.button("Submit Score", type="primary", use_container_width=True):
                if name.strip() == "":
                    st.error("Please enter a valid name.")
                else:
                    # Save score to local storage
                    ranking_data = localS.getItem("ranking")
                    if ranking_data is None:
                        ranking = {"chaos_mode": {}, "normal_mode": {}}
                    else:
                        ranking = eval(ranking_data)
                    
                    if chaos_mode:
                        ranking["chaos_mode"][name] = round(error, 2)
                    else:
                        ranking["normal_mode"][name] = round(error, 2)
                    localS.setItem("ranking", str(ranking))
                    
                    st.success(f"Score submitted! {name}: {error:.2f}%")
            
            abs_error = abs(error)
            
            if abs_error < 1.0:
                st.success("🎯 **PERFECT CUT!** 🎉")
                st.audio(audio_bytes, format="audio/mp3", start_time=0, autoplay=True)
                
                st.balloons()
                
            elif abs_error < 2.0:
                st.success("✨ **Super!** Great job! 👏")
                st.audio(audio_bytes, format="audio/mp3", start_time=0, autoplay=True)
                emoji_rain("👏") 
                
            elif abs_error < 5.0:
                st.info("👍 **Good attempt!** Keep refining!")
                emoji_rain("👍")
                st.audio(audio_bytes_lose, format="audio/mp3", start_time=0, end_time="5s",autoplay=True)
                
            elif abs_error < 10.0:
                st.audio(audio_bytes_lose, format="audio/mp3", start_time="15s", end_time="18s",autoplay=True)
                st.warning("⚠️ **Unbalanced Split** - Try again!")
                emoji_rain("⚠️")
                
            else:
                st.error("😠 **Very Unbalanced!** 💢")
                st.markdown("**Tip:** Use the Binary Search for guidance!")
                emoji_rain("💢") 
                st.audio(audio_bytes_lose, format="audio/mp3", start_time="15s", end_time="18s",autoplay=True)

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

# --- RANKING DISPLAY ---
st.divider()
st.markdown("### 🏅 Leaderboard")
ranking_data = localS.getItem("ranking")
if ranking_data is None:
    st.info("No scores submitted yet. Be the first to play and submit your score!")
else:
    ranking = eval(ranking_data)
    col_rank1, col_rank2 = st.columns(2)
    with col_rank1:
        st.markdown("#### 🔥 Chaos Mode")
        if len(ranking["chaos_mode"]) == 0:
            st.info("No scores submitted yet in Chaos Mode.")
        else:
            sorted_chaos = sorted(ranking["chaos_mode"].items(), key=lambda x: x[1])
            for i, (name, score) in enumerate(sorted_chaos, start=1):
                st.markdown(f"**{i}. {name}** - {score:.2f}% Error")
    with col_rank2:
        st.markdown("#### ⚖️ Normal Mode")
        if len(ranking["normal_mode"]) == 0:
            st.info("No scores submitted yet in Normal Mode.")
        else:
            sorted_normal = sorted(ranking["normal_mode"].items(), key=lambda x: x[1])
            for i, (name, score) in enumerate(sorted_normal, start=1):
                st.markdown(f"**{i}. {name}** - {score:.2f}% Error")


# --- SIDEBAR (Counter and Credits) ---
with st.sidebar:
    st.divider()
    
    st.markdown("### 🏆 The Team (NEMPA)")
    
    # Project Lead
    st.markdown("**Project Lead**")
    st.markdown("👨‍🏫 *Prof. Dr. Roberto Sant'Anna*")
    
    st.write("") # Spacer
    
    # Lead Dev
    st.markdown("**Lead Developer**")
    st.markdown("🛠️ *Enzo Ribeiro*")
    
    st.write("")
    
    # Core Dev (Technical Acknowledgment)
    st.markdown("**Core Developer**")
    st.markdown("🧠 *Ikaro Vieira*")
    
    st.write("")

    # Scientific Devs (Support Team)
    st.markdown("**Scientific Developers**")
    st.markdown("💻 *Felipe Brasileiro*")
    st.markdown("💻 *Iago Nunes*")

    st.divider()
    
    # Visitor Counter 
    st.markdown("### 🌍 Visitor Tracker")
    st.markdown("""
         <a href="https://info.flagcounter.com/50Hp">
                <img src="https://s01.flagcounter.com/count2/50Hp/bg_FFFFFF/txt_000000/border_CCCCCC/columns_2/maxflags_10/viewers_0/labels_0/pageviews_0/flags_0/percent_0/" 
                alt="Flag Counter" border="0">
                </a>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("© 2026 NEMPA - UFBA")