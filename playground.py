import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="Root Finder (Bisection)", layout="wide")
st.title("🎯 The Root Finder: Bisection Method")

# --- 1. Input ---
with st.sidebar:
    st.header("Parameters")
    
    function_string = st.text_input("Function f(x):", value="cos(x) - x")
    
    col1, col2 = st.columns(2)
    start_a = col1.number_input("Start (a):", value=0.0)
    end_b = col2.number_input("End (b):", value=1.0)
    
    max_iterations = st.slider("Max Iterations", 10, 100, 50)
    search_button = st.button("🔍 Find Root")

def evaluate_function(expression, x_val):
    # Allow common math names from the math module
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names.update({"x": x_val, "np": np})
    try:
        return eval(expression, {"__builtins__": {}}, allowed_names)
    except Exception:
        return None

# --- 2. Algorithm Logic ---
if search_button:
    # 2.1 Check Intermediate Value Theorem (IVT)
    f_a = evaluate_function(function_string, start_a)
    f_b = evaluate_function(function_string, end_b)

    if f_a is None or f_b is None:
        st.error("Function error! Check syntax (use 'x' as variable).")
    elif f_a * f_b > 0:
        st.error(f"⚠️ **Theorem failed!** f({start_a}) and f({end_b}) have the same sign.")
        st.write("The function does not cross the X-axis in this interval (or crosses an even number of times). Try another interval.")
    else:
        st.success("✅ **Condition accepted!** Function changes sign. Root exists.")
        
        # 2.2 Bisection Algorithm
        history = []
        low, high = start_a, end_b
        
        for i in range(max_iterations):
            mid = (low + high) / 2
            f_mid = evaluate_function(function_string, mid)
            
            history.append({
                "iter": i+1,
                "mid": mid,
                "error": (high - low) / 2
            })
            
            # Exact match check
            if abs(f_mid) < 1e-9: 
                break
                
            f_low = evaluate_function(function_string, low)
            if f_low * f_mid < 0:
                high = mid
            else:
                low = mid
        
        root = (low + high) / 2
        st.metric(label="Found Root (Approximate)", value=f"{root:.9f}")

        # --- 3. Visualization ---
        graph_col1, graph_col2 = st.columns(2)

        # Graph A: Function and Root
        with graph_col1:
            st.subheader("Function Visualization")
            fig, ax = plt.subplots()
            
            x_vals = np.linspace(start_a, end_b, 200)
            y_vals = [evaluate_function(function_string, x) for x in x_vals]
            
            ax.plot(x_vals, y_vals, label=f"f(x) = {function_string}", color='blue')
            ax.axhline(0, color='black', linewidth=1)
            ax.scatter([root], [0], color='red', s=100, zorder=5, label='Root')
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend()
            st.pyplot(fig)

        # Graph B: Error Convergence
        with graph_col2:
            st.subheader("Convergence Speed")
            errors = [h["error"] for h in history]
            iters = [h["iter"] for h in history]
            
            fig2, ax2 = plt.subplots()
            ax2.plot(iters, errors, color='green', marker='o', markersize=4)
            ax2.set_xlabel("Iteration")
            ax2.set_ylabel("Interval Size (Error)")
            ax2.set_title("Decreasing Interval (Binary Search)")
            ax2.set_yscale("log")
            ax2.grid(True, which="both", ls="-", alpha=0.5)
            st.pyplot(fig2)