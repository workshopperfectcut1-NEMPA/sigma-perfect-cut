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
3. **Chaos Mode:** Replaces the simple brownie (5 vertices) with a randomly generated polygon containing **300+ vertices**.

## 🧠 Mathematical Concepts

The project visualizes the **Intermediate Value Theorem (IVT)** applied to 2D geometry (often related to the _Pancake Theorem_).

- **Continuity:** As the knife moves across the shape, the area to the left changes continuously from 0% to 100%.
- **Topology:** Therefore, there must be a position where the area is exactly 50%.
- **Symmetry:** By rotating the angle, we explore the solution space (Cylindrical Topology) to find the cut where the error is zero.

## 💻 Tech Stack

- **Language:** Python 3.10+
- **Framework:** [Streamlit](https://streamlit.io/)
- **Geometry Engine:** [Shapely](https://shapely.readthedocs.io/)
- **Visualization:** Matplotlib

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

## 📚 Learning Resources

To deepen your understanding of the concepts behind this project, we recommend exploring the following resources:

### Mathematical Foundations

- **Intermediate Value Theorem (IVT):** [Khan Academy - IVT Introduction](https://www.khanacademy.org/math/calculus-1/cs1-limits-continuity/cs1-intermediate-value-theorem/v/intermediate-value-theorem)
- **Topology Basics:** [3Blue1Brown - Topology Fundamental Concepts](https://www.youtube.com/c/3Blue1Brown)

### Python

- **Python Course:** [Curso em Vídeo - YouTube Course](https://www.youtube.com/watch?v=S9uPNppGsGo&list=PLvE-ZAFRgX8hnECDn1v9HNTI71veL3oW0&index=2&t=2s)
- **Documentation:** [Python Documentation](https://docs.python.org/3/)
- **W3 Schools:** [W3 Schools Tutorial](https://www.w3schools.com/python/default.asp)

### Computational Geometry

- **Shapely Library:** [Official Shapely Documentation](https://shapely.readthedocs.io/)
- **Polygon Operations:** Learn about intersection, union, and area calculations
- **2D Geometry Algorithms:** Study ray casting, line segment intersection, and spatial partitioning

### Web Development with Streamlit

- **Streamlit Official Docs:** [streamlit.io](https://streamlit.io/)
- **Interactive Visualization:** [Streamlit Components and Plotting Guide](https://docs.streamlit.io/library/api-reference/charts)

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
