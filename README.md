#  Predator-Prey Simulation

A particle-based ecosystem simulation built with **Python** and **Pygame**, implementing emergent Lotka-Volterra dynamics through simple agent rules.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python) ![Pygame](https://img.shields.io/badge/Pygame-2.x-green?logo=pygame)

---

##  Overview

This simulation models a predator-prey ecosystem where blue **prey** particles and red **predator** particles interact in real time. Behaviors like flocking, hunting, fleeing, reproduction, and starvation emerge naturally from local rules — no global coordination needed.

---

##  Features

- **Prey (blue)**
  - Flock toward nearby prey
  - Flee from predators within detection radius
  - Seek and eat grass to gain energy and extend lifespan
  - Reproduce when colliding with another prey (if fed)
  - Die of old age or overpopulation

- **Predators (red)**
  - Hunt prey within detection radius
  - Wander when no prey is nearby
  - Seek mates when fed, to reproduce
  - Starve and die if hunger reaches zero
  - Hunger decreases faster when prey is scarce

- **Grass (green)**
  - Spawns randomly across the field
  - Consumed by prey on contact
  - Continuously regenerates over time

- **Physics**
  - Elastic collision resolution between particles
  - Velocity capping and friction damping
  - Wall bouncing

---

##  Project Structure

```
.
├── main.py         # Entry point — initializes Pygame, spawns particles, runs the game loop
├── particle.py     # Particle class — movement, forces, collision, drawing
└── universe.py     # Universe class — manages all particles, grass, detection, and reproduction
```

---

##  Getting Started

### Prerequisites

```bash
pip install pygame
```

### Running

```bash
python main.py
```

The simulation window title bar shows live counts:

```
Prey: 72  Predators: 11
```

---

##  Configuration

Key constants can be tweaked at the top of each file:

| Parameter | File | Default | Description |
|---|---|---|---|
| `WIDTH` / `HEIGHT` | all files | `800` | Window dimensions |
| `PREY0` | `main.py` | `50–100` | Initial prey count |
| `PREDATOR0` | `main.py` | `10–15` | Initial predator count |
| `RADIUS` | `particle.py` | `200` | Detection/interaction radius |
| `V0` | `particle.py` | `2` | Max particle speed |
| `FORCE` | `particle.py` | `0.15` | Steering force magnitude |

---

##  Behavioral Rules Summary

```
Prey:
  + Eat grass  → +energy, longer lifespan
  + Touch prey (if fed) → spawn new prey
  - Touched by predator → removed
  - Old age / overcrowding → removed

Predator:
  + Eat prey → hunger restored, eaten_prey++
  + Touch predator (both fed) → spawn new predator
  - hunger <= 0 → removed
```

---

##  Dependencies

- [Python 3.8+](https://www.python.org/)
- [Pygame 2.x](https://www.pygame.org/)

---
