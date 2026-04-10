# tracky — design.md

## 1. Overview

**tracky** is a virtual model railroad platform built around three interacting systems:

1. **Train simulation** — physically grounded movement along track (1D on a graph)
2. **Layout + world simulation** — grid-based environment with procedural growth
3. **Operational control** — layered control from manual driving to automated planning

The project is designed to grow incrementally, with each layer usable and testable on its own.

---

## 2. Core Principles

### 2.1 Physical, not abstract
Trains are not tokens. They:
- have position, velocity, and mass
- couple into consists
- require space and correct handling
- obey simple but believable motion rules

### 2.2 Separate worlds cleanly
- **Track world (graph)** → where trains move
- **Tile world (grid)** → where scenery and growth happen

These interact but remain independent.

### 2.3 Layered complexity
Each system is buildable in isolation:
- manual driving → assisted driving → planning → automation
- static layout → editable layout → procedural world

### 2.4 Build the toy first
Prioritize:
- visible behavior
- end-to-end slices
- minimal abstractions until needed

---

## 3. System Architecture

### 3.1 High-Level Components
+------------------------+ |      UI / Frontend     | +------------------------+ | +------------------------+
Simulation Engine
Track Graph
Train Physics
Coupling Model
Tile World
Rule Engine
AI / Control Layer
+------------------------+

---

## 4. Track & Layout System

### 4.1 Grid Layout

- World is a 2D grid of tiles
- Each tile may contain:
  - empty
  - track piece
  - terrain/scenery

### 4.2 Track Pieces

Basic types:
- straight
- curve
- switch (turnout)
- crossing (later)
- dead end

Each track piece defines:
- entry/exit directions
- connectivity rules

### 4.3 Track Graph

At runtime, track tiles form a **graph**:
- nodes: connection points
- edges: track segments

Each edge has:
- length
- curvature (optional)
- reference to tile(s)

Switches:
- dynamically change graph connectivity

---

## 5. Train Simulation

### 5.1 Representation

Each **car** has:
- length
- mass
- position along a track segment
- velocity
- coupling links (front/back)

A **locomotive** is a special car with:
- tractive force
- controls (throttle, brake, direction)

A **consist** is a connected set of cars.

---

### 5.2 Motion Model (1D)

Train motion is computed along track segments:

Per tick:
- compute net force:
  - locomotive tractive effort
  - braking force
  - rolling resistance
- update velocity
- update position along track
- transition across segments if needed

No full rigid-body simulation. Only longitudinal motion.

---

### 5.3 Coupling Model

Cars are connected via spring-like constraints:

- maintain target spacing
- transmit force through consist
- allow slack (optional later)

Operations:
- couple when:
  - adjacent
  - low relative speed
- uncouple:
  - split consist at boundary

---

### 5.4 Switch Interaction

- trains traverse switches based on current state
- must not:
  - pass through invalid branch
  - occupy conflicting routes (later)

---

## 6. Tile World & Procedural System

### 6.1 Tile Model

Each tile contains:
- **type** (grass, ballast, town, industry, etc.)
- **influence values** (hidden/internal):
  - traffic
  - ballast
  - vegetation
  - town
  - industry

---

### 6.2 Influence System

Each tick or step:
- values:
  - diffuse to neighbors
  - decay over time
  - reinforce each other

Examples:
- traffic ↑ → ballast ↑ → vegetation ↓
- station → town influence ↑
- low activity → vegetation regrows

---

### 6.3 Tile Transitions

Tiles change type based on thresholds:

Examples:
- grass → ballast → dirty ballast → yard
- grass → town → dense town
- unused ballast → overgrown

---

### 6.4 Seeds / Sources

Entities emit influence:
- trains → traffic
- stations → town
- industries → industrial
- forests → vegetation

---

## 7. Control & AI System

### 7.1 Layered Control Model

#### Layer 1: Manual Control
Player directly controls:
- throttle
- brake
- direction

#### Layer 2: Assisted Control
Primitive actions:
- `drive_to(target)`
- `stop_at(target)`
- `couple_to(car)`
- `uncouple()`

#### Layer 3: Maneuver Library
Reusable procedures:
- couple maneuver
- uncouple maneuver
- pull-clear
- runaround

#### Layer 4: Task Planning
Goal-based actions:
- fetch car
- assemble consist
- spot car at industry

Represented as DAG of tasks.

#### Layer 5 (future): Scheduling
- assign jobs
- coordinate multiple trains

---

### 7.2 World Representations

#### Physical World
- exact positions, velocities, couplings

#### Operational World
Derived facts:
- car on track
- cut composition
- track occupancy
- reachable segments

#### Task World
Goals:
- deliver car
- build train
- clear track

---

## 8. Play Modes

### 8.1 Manual Switching
- player drives locomotive
- solves yard puzzles

### 8.2 Sandbox Builder
- build layouts freely
- run trains

### 8.3 Procedural World Mode
- observe growth and interaction

### 8.4 (Future) Operations Mode
- assign tasks
- manage traffic

---

## 9. MVP (Vertical Slice)

### Goal
A minimal but complete toy:

- small fixed yard layout
- 1 locomotive
- 2–4 cars
- manual controls
- coupling/uncoupling
- 1 switch
- simple objective:
  - move a car to a target track

### Success Criteria
- feels like operating a train
- requires correct movement, not just routing

---

## 10. Milestone Plan

### Phase 1: Core Simulation
- track graph
- train movement
- coupling
- manual control

### Phase 2: Switching Gameplay
- objectives
- basic UI
- small yard scenarios

### Phase 3: Layout Builder
- place track
- save/load layouts

### Phase 4: Procedural World
- tile system
- influence spreading
- visible environment changes

### Phase 5: Assisted Control
- autopilot primitives

### Phase 6: Planning
- basic task execution
- simple switching automation

---

## 11. Testing Strategy

Focus on:
- invariants:
  - no overlap
  - valid coupling
  - valid graph traversal
- scenario tests:
  - coupling works
  - switching puzzle solvable
- manual sandbox testing

Avoid:
- excessive micro unit tests
- over-mocking

---

## 12. Open Questions

- How much coupling slack to simulate?
- How precise should stopping behavior be?
- When to introduce signals / collision avoidance?
- How complex should tile rules become?
- How far to push AI planning vs keeping it simple?

---

## 13. Non-Goals (for now)

- full signaling systems
- multiplayer
- high-fidelity physics
- complex 3D graphics
- large-scale dispatching

---

## 14. Summary

tracky is a system-first project:

- a **train simulation core**
- a **procedural world layer**
- a **growing control/AI stack**

Each layer builds on the last, creating a platform that can evolve from a small switching toy into a rich railroad sandbox.
