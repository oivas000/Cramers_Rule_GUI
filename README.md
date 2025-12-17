# 🧮 Cramer's Rule Solver

A high-performance, interactive web application built with **Python**, **NiceGUI**, and **NumPy** to solve systems of $n \times n$ linear equations using Cramer's Rule. Designed with a focus on educational clarity and a modern "Neon" aesthetic.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge)
![NiceGUI](https://img.shields.io/badge/GUI-NiceGUI-green.svg?style=for-the-badge)
![NumPy](https://img.shields.io/badge/math-NumPy-orange.svg?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)

## 🚀 Overview

Solving systems of linear equations is a fundamental task in engineering and mathematics. This tool provides an intuitive interface to input matrices, calculate determinants, and view a detailed, step-by-step mathematical breakdown of the solution.

### Key Features:
* **Dynamic Grid:** Supports systems from $2 \times 2$ up to $18 \times 18$.
* **Detailed Steps:** Visualizes the determinant of the coefficient matrix ($det(A)$) and all replacement matrices ($det(A_i)$).
* **Dual Themes:** Fully functional "Neon Dark" and "Clean Light" modes.
* **Responsive Design:** Optimized for both mobile and desktop viewing.
* **Smart State Management:** Persists your matrix data even when changing themes or grid sizes.

---

## 📐 The Mathematics

Cramer's Rule states that for a system of equations $Ax = B$, each variable $x_i$ is given by:

$$x_i = \frac{\text{det}(A_i)}{\text{det}(A)}$$

Where $A_i$ is the matrix formed by replacing the $i$-th column of $A$ with the column vector $B$.



---

## 🛠️ Installation & Usage

### Prerequisites
* Python 3.8 or higher
* `pip` (Python package manager)

### 1. Clone the Repository
```bash
git clone [https://github.com/oivas000/Cramers_Rule_GUI.git](https://github.com/oivas000/Cramers_Rule_GUI.git)
cd Cramers_Rule_GUI