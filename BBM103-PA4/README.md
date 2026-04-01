### 📂 BBM103-assignment4 (Route Finder) İçin
Klasörün içindeki `README.md` içeriğini şununla değiştir:

```markdown
# 🛣️ Route Finder (Sinkhole Simulation)

A pathfinding application that calculates the shortest (cheapest) route across a field with environmental hazards (sinkholes).

## ✨ Key Features
* **Pathfinding Algorithm:** Uses **Recursion** and **Backtracking** to find the optimal path from left to right.
* **Dynamic Cost Calculation:** Evaluates three different movement costs based on proximity to horizontal, vertical, or diagonal sinkholes.
* **Optimization:** Implements **Memoization** to handle large grids efficiently and prevent redundant calculations.
* **Deterministic Logic:** Strictly follows movement priorities (Right > Upper > Lower > Left) to ensure consistent results.

## 🛠 Technical Stack
* **Language:** Python 3.9
* **Core Concepts:** Recursive algorithms, Memoization, and Grid manipulation

## 🚀 Execution
```bash
python3 route_finder.py input.txt output.txt
