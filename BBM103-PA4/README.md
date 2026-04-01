```markdown
# 🛣️ Route Finder 

A pathfinding application that calculates the shortest (cheapest) route across a field with environmental hazards (sinkholes)[cite: 437, 440].

## ✨ Key Features
* **Pathfinding Algorithm:** Uses **Recursion** and **Backtracking** to find the optimal path from left to right[cite: 463, 466, 474].
* **Dynamic Cost Calculation:** Evaluates three different movement costs based on proximity to horizontal, vertical, or diagonal sinkholes[cite: 448, 449, 450, 451, 452].
* **Optimization:** Implements **Memoization** to handle large grids efficiently and prevent redundant calculations.
* **Deterministic Logic:** Strictly follows movement priorities (Right > Upper > Lower > Left) to ensure consistent results[cite: 464, 465, 466].

## 🛠 Technical Stack
* **Language:** Python 3.9[cite: 432, 492].
* **Core Concepts:** Recursive algorithms, Memoization, and Grid manipulation[cite: 451, 463, 474].

## 🚀 Execution
```bash
python3 route_finder.py input.txt output.txt
