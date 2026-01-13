from shapely.geometry import Polygon
from shapely.affinity import rotate, translate
import numpy as np
import streamlit as st
import random 


def create_brownie():
    """Creates the brownie polygon"""
    brownie_coords = [(-2, -2), (1, -3), (3, 0), (2, 3), (-3, 2)]
    return Polygon(brownie_coords)

# def create_complex_polygon(num_vertices=1000):
#     """Creates a complex polygon with a specified number of vertices."""
#     # angles = np.linspace(0, 2 * np.pi, num_vertices, endpoint=False)
#     angles = np.sort(np.random.uniform(0, 2*np.pi, num_vertices))
#     radius = np.random.uniform(1, 3, num_vertices)  # Random radius for complexity
#     points = [(r * np.cos(a), r * np.sin(a)) for r, a in zip(radius, angles)]
#     print('complex polygon created with', num_vertices, 'vertices')
#     return Polygon(points)

def create_complex_polygon(num_vertices=300): # Aumentei um pouco os vértices pra ficar liso
    angles = np.linspace(0, 2 * np.pi, num_vertices, endpoint=False)
    
    # --- AJUSTE DE "DRAMA" ---
    
    # 1. Base menor: O "centro" seguro é pequeno
    base_radius = 2.0 
    
    # 2. Onda Lenta (Assimetria Global): Deixa a figura oval/torta
    # Aumentei a força aqui (antes era máx 1.5)
    wave_slow = np.random.uniform(1.0, 2.0) * np.sin(angles + np.random.uniform(0, 2*np.pi))
    
    # 3. Onda Rápida (Os Raios/Pontas): Aqui é o segredo dos raios grandes!
    # Escolhemos aleatoriamente entre 4 a 8 pontas grandes
    num_spikes = np.random.randint(4, 9) 
    # Amplitude alta para criar "vales" fundos e "picos" altos
    wave_spikes = np.random.uniform(1.5, 3.0) * np.sin(num_spikes * angles + np.random.uniform(0, 2*np.pi))
    
    # Soma tudo
    radius = base_radius + wave_slow + wave_spikes
    
    # Adiciona um ruído fino só pra deixar a borda "crocante"
    noise = np.random.uniform(-0.3, 0.3, num_vertices)
    radius += noise
    
    # IMPORTANTE: Clip para 0.2 para garantir que o raio nunca seja negativo (o que cruzaria o centro)
    radius = np.clip(radius, 0.2, None)

    points = [(r * np.cos(a), r * np.sin(a)) for r, a in zip(radius, angles)]
    
    # Rotaciona para variar a posição inicial
    poly = Polygon(points)
    return rotate(poly, np.random.uniform(0, 360), origin='centroid')



def create_knife(position, angle):
    """
    Creates the knife geometry (infinite half-plane)
    
    Args:
        position: Horizontal position of the knife
        angle: Rotation angle in degrees
    
    Returns:
        Polygon: Knife geometry
    """
    knife_base = Polygon([(-10, -10), (-10, 10), (0, 10), (0, -10)])
    knife_translated = translate(knife_base, xoff=position)
    knife_rotated = rotate(knife_translated, angle, origin=(0, 0))
    return knife_rotated


def calculate_cut(brownie, position, angle):
    """
    Calculates the cut area
    
    Args:
        brownie: Brownie polygon
        position: Knife position
        angle: Knife angle
    
    Returns:
        tuple: (cut piece, cut area)
    """
    knife = create_knife(position, angle)
    piece = brownie.intersection(knife)
    cut_area = piece.area
    return piece, cut_area


def calculate_error(cut_area, total_area):
    """
    Calculates the percentage error relative to the perfect cut (50%)
    
    Args:
        cut_area: Cut area
        total_area: Total brownie area
    
    Returns:
        float: Percentage error
    """
    target_area = total_area / 2
    error = (abs((cut_area - target_area)) / target_area) * 100
    return error


def optimized_binary_search(brownie, angle, min_pos=-4.0, max_pos=4.0, num_iterations=20):
    """
    Executes binary search to find the optimal cut position
    
    Args:
        brownie: Brownie polygon
        angle: Knife angle (fixed during search)
        min_pos: Initial minimum position
        max_pos: Initial maximum position
        num_iterations: Number of iterations
    
    Returns:
        dict: {
            'optimal_position': float,
            'position_history': list,
            'error_history': list,
            'area_history': list
        }
    """
    total_area = brownie.area
    target_area = total_area / 2
    
    position_history = []
    error_history = []
    area_history = []
    
    for i in range(num_iterations):
        mid_pos = (min_pos + max_pos) / 2
        _, cut_area = calculate_cut(brownie, mid_pos, angle)
        error = calculate_error(cut_area, total_area)
        
        # Store history
        position_history.append(mid_pos)
        error_history.append(error)
        area_history.append(cut_area)
        
        # Adjust interval
        if cut_area < target_area:
            min_pos = mid_pos
        else:
            max_pos = mid_pos
    
    optimal_position = (min_pos + max_pos) / 2
    
    return {
         "optimal_position": optimal_position,
        "position_history": position_history,
        "error_history": error_history,
        "area_history": area_history
    }


def emoji_rain(emoji_text: str, count: int = 40):
    """
    Creates a falling rain animation effect with the specified emoji using CSS/HTML.

    Args:
        emoji_text: The emoji character to use for the rain (e.g., "👏", "🔥")
        count: The number of emoji particles to generate. Defaults to 40.

    Returns:
        None: This function renders the animation directly to the Streamlit interface using st.markdown.
    """
    css_style = """
    <style>
    .emoji-rain {
        position: fixed;
        top: -10%;
        z-index: 99999;
        user-select: none;
        pointer-events: none;
        animation-name: fall;
        animation-timing-function: ease-in;
        animation-fill-mode: forwards;
    }
    @keyframes fall {
        0% { top: -10%; opacity: 1; }
        100% { top: 100vh; opacity: 0; transform: rotate(20deg); }
    }
    </style>
    """
    
    emojis_html = ""
    for _ in range(count):
        left = random.randint(0, 100)
        duration = random.uniform(1.5, 3.5)
        delay = random.uniform(0, 1.0)
        size = random.randint(20, 50)
        
       
        emojis_html += f"""<div class="emoji-rain" style="left: {left}%; animation-duration: {duration}s; animation-delay: {delay}s; font-size: {size}px;">{emoji_text}</div>"""
    
    
    full_html = css_style + emojis_html
    st.markdown(full_html, unsafe_allow_html=True)