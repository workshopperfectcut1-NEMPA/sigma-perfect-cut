# 🇺🇸 [English](README.md) | [🇧🇷 Português](README.pt-BR.md)

# 🔪 Codificando o Corte Perfeito

### Workshop SigmaCamp 2026 | NEMPA - UFBA

**Codificando o Corte Perfeito** é uma aplicação web interativa desenvolvida para demonstrar conceitos de **Topologia Algébrica** e **Complexidade de Algoritmos** por meio de um desafio geométrico gamificado.

Esta ferramenta foi desenvolvida pelo **Núcleo de Estudos em Matemática Pura e Aplicada (NEMPA)** da Universidade Federal da Bahia (UFBA) para o **Workshop Internacional de STEM SigmaCamp 2026**.

🔗 **Demonstração ao vivo:** [sigma-perfect-cut.streamlit.app](https://sigma-perfect-cut.streamlit.app/)

---

## 🎯 O Desafio

O objetivo é simples, porém matematicamente profundo: **dividir um polígono irregular (um “brownie”) em duas áreas iguais utilizando um único corte reto.**

Os usuários enfrentam um duelo: **Intuição Humana vs. Precisão da Máquina.**

1. **Modo Manual:** O usuário tenta encontrar o corte perfeito ajustando os controles de ângulo e posição.
2. **Modo Algoritmo:** A máquina resolve o problema utilizando **Busca Binária**, demonstrando o poder da complexidade logarítmica ($O(\log n)$).
3. **Modo Caos:** Substitui o brownie simples (5 vértices) por um polígono gerado aleatoriamente contendo **mais de 300+ vértices**.

## 🧠 Conceitos Matemáticos

O projeto visualiza o **Teorema do Valor Intermediário (TVI)** aplicado à geometria bidimensional (frequentemente relacionado ao _Teorema da Panqueca_).

- **Continuidade:** À medida que a faca se move sobre a forma, a área à esquerda varia continuamente de 0% a 100%.
- **Topologia:** Portanto, deve existir uma posição em que a área seja exatamente 50%.
- **Simetria:** Ao rotacionar o ângulo, exploramos o espaço de soluções (Topologia Cilíndrica) para encontrar o corte onde o erro é zero.

## 💻 Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Framework:** [Streamlit](https://streamlit.io/)
- **Motor Geométrico:** [Shapely](https://shapely.readthedocs.io/)
- **Visualização:** Matplotlib

## 🚀 Como Executar Localmente

**1. Clone o repositório:**

```bash
git clone https://github.com/NEMPA-UFBA/sigma-perfect-cut.git
cd sigma-perfect-cut
```

**2. Crie um ambiente virtual:**

```bash
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
```

**3. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**Execute a aplicação:**

```bash
streamlit run app.py
```

## 📚 Recursos de Aprendizado

Para aprofundar sua compreensão sobre os conceitos por trás deste projeto, recomendamos explorar os seguintes recursos:

### Fundamentos Matemáticos

- **Teorema do Valor Intermediário (TVI):** [Khan Academy - Introdução ao TVI](https://www.khanacademy.org/math/calculus-1/cs1-limits-continuity/cs1-intermediate-value-theorem/v/intermediate-value-theorem)
- **Fundamentos de Topologia:** [3Blue1Brown - Conceitos Fundamentais de Topologia](https://www.youtube.com/c/3Blue1Brown)

### Python

- **Curso em Vídeo:** [Curso em Vídeo - YouTube](https://www.youtube.com/watch?v=S9uPNppGsGo&list=PLvE-ZAFRgX8hnECDn1v9HNTI71veL3oW0&index=2&t=2s)
- **Documentação:** [Documentação Python](https://docs.python.org/pt-br/)
- **W3 Schools:** [Tutorial W3 Schools](https://www.w3schools.com/python/default.asp)

### Geometria Computacional

- **Biblioteca Shapely:** [Documentação Oficial do Shapely](https://shapely.readthedocs.io/)
- **Operações com Polígonos:** Aprenda sobre intersecção, união e cálculos de área
- **Algoritmos de Geometria 2D:** Estude ray casting, intersecção de segmentos de reta e particionamento espacial

### Desenvolvimento Web com Streamlit

- **Documentação Oficial Streamlit:** [streamlit.io](https://streamlit.io/)
- **Visualização Interativa:** [Guia de Componentes e Gráficos do Streamlit](https://docs.streamlit.io/library/api-reference/charts)

---

## 👥 A Equipe (NEMPA – UFBA)

**Coordenação do Projeto**

- [Prof. Roberto Sant'Anna](https://github.com/rbtsantanna)

**Desenvolvedor Líder**

- [Enzo Ribeiro](https://github.com/enzoribeirodev)

**Equipe de Desenvolvimento**

- [Ikaro Vieira](https://github.com/Ikarosv)
- [Felipe Brasileiro](https://github.com/felipebr-s)
- [Iago Nunes](https://github.com/iagomatta1505)

---

© 2026 **NEMPA – Núcleo de Estudos em Matemática Pura e Aplicada**.  
Todos os direitos reservados.
