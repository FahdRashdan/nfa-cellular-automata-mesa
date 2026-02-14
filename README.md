# NFA Cellular Automata Simulation (Mesa)

## Overview

This project is an interactive simulation that combines:

* **Cellular Automata (CA)** — a grid of cells that evolve over time
* **Non-Deterministic Finite Automata (NFA)** — each cell behaves like a state machine
* **Mesa Agent-Based Modeling Framework** — used for simulation and visualization

Each cell is an intelligent agent that changes its state based on:

* Its current state
* Its neighbors
* Probabilistic NFA transitions
* User-controlled parameters

The simulation runs in a web interface with real-time visualization and charts.

---

## Features

* 20 × 20 interactive grid (400 agents)
* Real-time visualization
* Real-time state statistics chart
* Non-deterministic state transitions
* Interactive parameter sliders
* Dynamic NFA transition rewiring
* Ability to disable chaotic behavior
* Toroidal grid (edges wrap around)

---

## Technologies Used

* Python 3
* Mesa Framework
* Agent-Based Modeling
* Cellular Automata
* Non-Deterministic Finite Automata
* Web Visualization (Mesa ModularServer)

---

## Project Structure

```
project_folder/

run.py        → Launches visualization and server
model.py      → Defines the NFACAModel
agent.py      → Defines the NFACellAgent
README.md     → Project documentation
```

---

## Installation

### Step 1 — Install Python

Make sure Python 3.8 or newer is installed:

```
python --version
```

---

### Step 2 — Install Mesa

Install Mesa using pip:

```
pip install mesa
```

---

### Step 3 — Place Files Together

Make sure these files are in the same folder:

```
run.py
model.py
agent.py
```

---

## How to Run the Simulation

Open terminal in the project folder and run:

```
python run.py
```

Then open your browser and go to:

```
http://127.0.0.1:8521
```

---

## Agent States

Each agent can be in one of four states:

| State   | Color  | Meaning           |
| ------- | ------ | ----------------- |
| Alive   | Green  | Active / healthy  |
| Dying   | Red    | Decaying          |
| Stable  | Purple | Balanced          |
| Chaotic | Gray   | Random / unstable |

---

## How the System Works

Each simulation step:

1. Each agent checks its 8 neighbors
2. Counts how many are Alive
3. Converts that into an input symbol:

   * L → Low density
   * M → Medium density
   * H → High density
4. Uses the NFA transition table
5. Chooses next state (probabilistic if multiple options)
6. All agents update simultaneously

---

## Interactive Controls

The web interface includes sliders:

### Initial Alive Ratio

Controls how many agents start as Alive

Range: 0.0 – 1.0

---

### Branching Probability

Controls randomness in NFA transitions

Higher value → more predictable
Lower value → more random

---

### Chaos Bias

Controls preference toward Chaotic transitions

Low value → less chaos
High value → more chaos

---

### Disable Chaotic State

0 → Chaotic enabled
1 → Chaotic disabled

---

## Visualization

The interface shows:

* Grid with colored agents
* Real-time chart of state counts
* Interactive controls
* Live simulation updates

---

## Model Components

### NFACellAgent

Represents one grid cell.

Responsible for:

* Reading neighbors
* Computing next state
* Applying state updates

---

### NFACAModel

Responsible for:

* Creating grid
* Creating agents
* Managing simulation steps
* Managing NFA transitions
* Collecting statistics

---

### run.py

Responsible for:

* Visualization
* UI sliders
* Server launch

---

## Simulation Logic Summary

This project combines:

* Cellular Automata structure
* Finite Automata logic
* Probabilistic transitions
* Agent-Based Modeling
* Interactive visualization

---

## Example Applications

This model can represent:

* Biological systems
* Disease spread
* Ecosystems
* Complex systems
* Network behavior
* Artificial life simulations

---

## How to Modify

You can easily change:

* Grid size (in model.py)
* Transition rules
* Colors
* States
* Probabilities
* Visualization settings

---

## Troubleshooting

### Problem: Mesa not found

Solution:

```
pip install mesa
```

---

### Problem: Server not opening

Make sure port 8521 is not in use.

---

### Problem: Blank grid

Make sure all files are in same folder.

---

## Author

Developed as a Cellular Automata + NFA simulation using Mesa.

---

## License

Free for educational and research use.

---

## Summary

This project demonstrates a powerful combination of:

* Cellular Automata
* Non-Deterministic Finite Automata
* Agent-Based Modeling
* Interactive simulation

with real-time visualization and full user control.
