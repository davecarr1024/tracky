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

### 12.1 Coupling Mechanics

- **Slack model**: Should coupling be rigid (no slack) initially, with slack added later, or should a small fixed slack be present from the start? Rigid is simpler but feels wrong for switching; slack adds complexity but matters for realism.
- **Constraint resolution order**: When a consist has multiple coupled cars, in what order do forces propagate? Push from rear vs. pull from front may need different handling.
- **Coupling detection**: What proximity and relative-speed thresholds trigger automatic coupling? Should the player initiate coupling explicitly (button press when close) or should it happen on contact?
- **Consist integrity**: If a car is coupled front-and-rear (e.g., sandwiched), how is force propagated through it vs. around it?

### 12.2 Switch State and Control

- **Switch ownership**: Who controls a switch — the player directly, the locomotive (as it approaches), or a separate operator layer? All three are valid design choices with different gameplay feels.
- **Switch locking**: Should a switch lock while a train is occupying it? This is realistic but adds complexity.
- **Derailment**: Should traversing a switch in the wrong position be an error, derail the train, or be silently ignored? Derailment adds stakes but requires recovery mechanics.
- **Switch memory**: Does a switch return to a default position or stay where last thrown?

### 12.3 Stopping and Positioning

- **Stopping precision**: The current physics model uses continuous damping. Is this precise enough for spotting cars at industries, or does it need a "creep and stop" low-speed mode?
- **Gravity**: Should grade/slope affect speed? This is out of scope for a flat grid but worth keeping in mind.
- **Collision**: Should cars physically block each other, or is that deferred? Collision detection on a 1D track graph is simpler than in 2D but still needs careful handling.

### 12.4 Rendering and Visuals

- **Curved rendering**: Curved connections are currently approximated geometrically via `Projection.connection_lerp()`. Should curves be rendered as actual Bezier/arc segments, or is the current linear interpolation sufficient?
- **Car rendering**: Cars span multiple connections (their length can cross piece boundaries). How should a car that straddles a curve and a straight be rendered?
- **Camera**: Should the viewport be fixed, or should it pan/zoom to follow the locomotive?
- **Visual fidelity**: Pure colored rectangles and lines? Pixel art sprites? This affects scope significantly.

### 12.5 Tile World

- **Tile vs. track decoupling**: The design separates the tile grid from the track graph. Is this the right call, or should track pieces carry all tile metadata directly? The current `Piece` class has no tile-type concept.
- **Influence resolution order**: During diffusion, should all tiles update simultaneously (double-buffered) or in scan order? Simultaneous is correct but requires extra memory.
- **Tile rules complexity**: Rules like "traffic ↑ → ballast ↑ → vegetation ↓" are easy to say but hard to tune. How will rules be authored — hardcoded, data-driven, or scripted?
- **Performance**: With a large grid and per-tick influence spreading, will Python be fast enough, or does this need numpy or a compiled extension?

### 12.6 Control and AI

- **`drive_to` implementation**: The assisted control layer needs to know the distance to a target on the track graph. Is shortest-path distance straightforward given the current graph representation, or is Dijkstra needed?
- **Deadlock handling**: Switching puzzles can deadlock (no legal moves). Should the puzzle designer prevent this, or should the solver detect and report it?
- **AI depth**: How far should the task planner go? A simple BFS/DFS over maneuver steps is achievable. Full STRIPS-style planning is probably overkill. What's the right level?
- **Mixed control**: When the AI is executing a plan, what input can the player override? Full override? Pause only? This affects how the control layers interact.

### 12.7 Save / Load and Layout

- **Serialization format**: JSON is the obvious choice for layouts. What is the canonical representation of a `Piece` (position + connection directions + switch state)?
- **Versioning**: How will save files evolve as the game changes? A schema version field from the start avoids pain later.
- **Layout validation**: When loading a layout, what checks are required to ensure the graph is consistent?

### 12.8 Architecture

- **Consist as first-class object**: The current `Car` / `CarManager` model treats all cars identically. Should `Consist` be a separate class managed by a `ConsistManager`, or should consist membership be derived dynamically from coupling links?
- **Switch piece representation**: The current `Piece` / `Connection` model can represent switch topologies (multiple connections in same direction), but switch state (which branch is active) is not yet modeled. Where does switch state live — on `Piece`, on a separate `Switch` entity, or on the `Grid`?
- **Locomotive vs. Car**: Should `Locomotive` be a subclass of `Car` or a separate entity that wraps a car? Subclassing is simpler; composition is more flexible if locomotives can be swapped.
- **Simulation tick rate**: The current `update(t, dt)` interface is flexible. Should the sim target a fixed timestep (e.g., 60 Hz physics) with interpolation for rendering, or is variable timestep acceptable?

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
