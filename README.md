# 🇺🇸 [English](README.md) | [🇧🇷 Português](README.pt-BR.md)

# 🔪 Coding the Perfect Cut
### SigmaCamp 2026 Workshop | NEMPA - UFBA

**Coding the Perfect Cut** is an interactive web application designed to demonstrate concepts of **Algebraic Topology** and **Algorithm Complexity** through a gamified geometric challenge.

This tool was developed by the **Center for Studies in Pure and Applied Mathematics (NEMPA)** at the Federal University of Bahia (UFBA) for the **SigmaCamp 2026** International STEM Workshop.

🔗 **Live Demo:** [sigma-perfect-cut.streamlit.app](https://sigma-perfect-cut.streamlit.app/)

---

## 🎯 The Challenge
The goal is simple yet mathematically profound: **Divide an irregular polygon (a "brownie") into two equal areas using a single straight cut.**

Users face a duel: **Human Intuition vs. Machine Precision.**

1. **Manual Mode:** The user tries to find the perfect cut by adjusting the angle and position sliders.
2. **Algorithm Mode:** The machine solves the problem using **Binary Search**, demonstrating the power of logarithmic complexity ($O(\log n)$).

## 🧠 Mathematical Concepts
The project visualizes the **Intermediate Value Theorem (IVT)** applied to 2D geometry (often related to the *Pancake Theorem*).

* **Continuity:** As the knife moves across the shape, the area to the left changes continuously from 0% to 100%.
* **Topology:** Therefore, there must be a position where the area is exactly 50%.
* **Symmetry:** By rotating the angle, we explore the solution space (Cylindrical Topology) to find the cut where the error is zero.

## 💻 Tech Stack
* **Language:** Python 3.10+
* **Framework:** [Streamlit](https://streamlit.io/)
* **Geometry Engine:** [Shapely](https://shapely.readthedocs.io/)
* **Visualization:** Matplotlib

## 🚀 How to Run Locally

**1. Clone the repository:**
```bash
git clone [https://github.com/NEMPA-UFBA/sigma-perfect-cut.git](https://github.com/NEMPA-UFBA/sigma-perfect-cut.git)
cd sigma-perfect-cut
```

**2. Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run the app:**
```bash
streamlit run app.py
```

## 👥 The Team (NEMPA – UFBA)

**Project Lead**  
- [Prof. Roberto Sant'Anna](https://github.com/rbtsantanna)  

**Lead Developer**  
- [Enzo Ribeiro](https://github.com/enzoribeirodev)  

**Development Team**  
- [Ikaro Vieira](https://github.com/Ikarosv)  
- [Felipe Brasileiro](https://github.com/felipebr-s)  
- [Iago Nunes](https://github.com/iagomatta1505)  

---

© 2026 **NEMPA – Núcleo de Estudos em Matemática Pura e Aplicada**.  
All rights reserved.