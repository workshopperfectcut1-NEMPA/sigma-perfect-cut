import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# Configuração da Página
st.set_page_config(page_title="Caçador de Raízes (Bisseção)", layout="wide")
st.title("🎯 O Caçador de Raízes: Método da Bisseção")

# --- 1. Entrada de Dados ---
with st.sidebar:
    st.header("Parâmetros")
    # O usuário digita a função como string
    func_str = st.text_input("Função f(x):", value="cos(x) - x")
    
    # Intervalo
    col1, col2 = st.columns(2)
    a_in = col1.number_input("Início (a):", value=0.0)
    b_in = col2.number_input("Fim (b):", value=1.0)
    
    iterations = st.slider("Máximo de Iterações", 10, 100, 50)
    run_btn = st.button("🔍 Buscar Raiz")

# Função segura para avaliar string matemática
def evaluate_function(expression, x_val):
    # Permite usar nomes matemáticos comuns
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names.update({"x": x_val, "np": np})
    try:
        return eval(expression, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        return None

# --- 2. Lógica do Algoritmo ---
if run_btn:
    # 2.1 Verifica Teorema do Valor Intermediário (TVI)
    fa = evaluate_function(func_str, a_in)
    fb = evaluate_function(func_str, b_in)

    if fa is None or fb is None:
        st.error("Erro na função! Verifique a sintaxe (use 'x' como variável).")
    elif fa * fb > 0:
        st.error(f"⚠️ **O Teorema falhou!** f({a_in}) e f({b_in}) têm o mesmo sinal.")
        st.write("A função não cruza o eixo X neste intervalo (ou cruza um número par de vezes). Tente outro intervalo.")
    else:
        st.success("✅ **Condição aceita!** A função muda de sinal. A raiz existe.")
        
        # 2.2 Algoritmo de Bisseção (Com Histórico)
        history = []
        low, high = a_in, b_in
        
        for i in range(iterations):
            mid = (low + high) / 2
            f_mid = evaluate_function(func_str, mid)
            
            history.append({
                "iter": i+1,
                "mid": mid,
                "error": (high - low) / 2
            })
            
            if abs(f_mid) < 1e-9: # Achou exato (raro)
                break
                
            # Lógica de Decisão
            f_low = evaluate_function(func_str, low)
            if f_low * f_mid < 0:
                high = mid
            else:
                low = mid
        
        # Resultado Final
        root = (low + high) / 2
        st.metric(label="Raiz Encontrada (Aproximada)", value=f"{root:.9f}")

        # --- 3. Visualização ---
        col_graph1, col_graph2 = st.columns(2)

        # Gráfico A: A Função e a Raiz
        with col_graph1:
            st.subheader("Visualização da Função")
            fig, ax = plt.subplots()
            
            # Cria pontos para plotar
            x_vals = np.linspace(a_in, b_in, 200)
            # Truque para vetorizar a função string do usuário
            y_vals = [evaluate_function(func_str, x) for x in x_vals]
            
            ax.plot(x_vals, y_vals, label=f"f(x) = {func_str}", color='blue')
            ax.axhline(0, color='black', linewidth=1) # Eixo X
            ax.scatter([root], [0], color='red', s=100, zorder=5, label='Raiz') # A bolinha vermelha
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend()
            st.pyplot(fig)

        # Gráfico B: Convergência do Erro
        with col_graph2:
            st.subheader("Velocidade de Convergência")
            errors = [h["error"] for h in history]
            iters = [h["iter"] for h in history]
            
            fig2, ax2 = plt.subplots()
            ax2.plot(iters, errors, color='green', marker='o', markersize=4)
            ax2.set_xlabel("Iteração")
            ax2.set_ylabel("Tamanho do Intervalo (Erro)")
            ax2.set_title("O Intervalo Diminuindo (Busca Binária)")
            ax2.set_yscale("log") # Escala logarítmica para mostrar a potência!
            ax2.grid(True, which="both", ls="-", alpha=0.5)
            st.pyplot(fig2)