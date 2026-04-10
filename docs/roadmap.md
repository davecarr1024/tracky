# tracky — roadmap.md

## Current State Assessment

### What Is Implemented

#### Core Abstractions (`tracky/core/`)
- `Error` / `Errorable`: typed, context-rich exceptions with chaining — **complete**
- `Validatable`: deferred invariant-checking framework with pause/resume — **complete**

#### Track Graph (`tracky/track/`)
- Grid coordinate system: `Position`, `Direction`, `Rotation` — **complete**
- `Grid`: 2D tile map with piece insertion/removal, bounds, ASCII debug, loop factory — **complete**
- `Connection`: directional track edges with forward/reverse navigation and shape metadata — **complete**
- `Piece`: grid tile with connections, rotation, neighbor access — **complete**
- `TrackPosition`: parameterized position on a connection with seamless cross-piece movement — **complete**
- Factory helpers: `Grid.create_loop`, `Piece.create_line` — **complete**

#### Train Physics (`tracky/cars/`)
- `Car`: position on track, velocity, mass, damping friction, force/impulse application — **complete**
- `CarManager`: collection with batch `update(t, dt)` — **complete**

#### Simulation (`tracky/sim/`)
- `Sim`: top-level orchestrator (grid + car manager) — **complete (thin wrapper)**

#### Visuals (`tracky/visuals/`)
- Screen-space math: `Position`, `Offset`, `Rotation`, `Rectangle` — **complete**
- `Projection`: grid ↔ screen coordinate conversion, tile geometry, connection rendering (straight and curved) — **complete**
- `Visualizer`: Pygame window with update loop — **stub (render_piece is empty)**

#### Test Suite
- 60+ tests across all modules — **comprehensive**
- Strict pyright type checking — **passing**
- ruff linting, black formatting — **passing**

---

### What Is Designed But Not Implemented

The following are described in `docs/design.md` but have no code:

| System | Status | Notes |
|--------|--------|-------|
| Track rendering | Stub | `_render_piece` exists but draws nothing |
| Switch state | Missing | Pieces support switch topology but no state or control |
| Coupling model | Missing | No coupling links, slack, or constraint propagation |
| Locomotive / throttle | Missing | No controls, only bare Car with force API |
| Consist abstraction | Missing | No grouping of coupled cars |
| Manual control input | Missing | No keyboard/input handling in Visualizer |
| Tile world | Missing | No tile types, influence values, or decay |
| Influence spreading | Missing | No tick-based neighbor diffusion |
| Tile transitions | Missing | No threshold-based type changes |
| Assisted control layer | Missing | No `drive_to`, `stop_at`, etc. |
| Maneuver library | Missing | No runaround, couple maneuver, pull-clear |
| Task planning | Missing | No goal-based DAG execution |
| Switching objectives | Missing | No puzzle or win conditions |
| Layout builder | Missing | No interactive tile placement |
| Save/load | Missing | No serialization |

---

## Phased Implementation Plan

The plan below follows the milestone structure from `design.md`, refined with concrete implementation steps based on current code.

---

### Phase 1: Visible Railroad (MVP Slice)

**Goal**: A running simulation you can watch and interact with.

The physics and graph are solid. The gap is that nothing renders or responds to input. Close this gap first so the project has a working toy to iterate on.

#### 1a — Track Rendering
- Implement `Visualizer._render_piece(piece, rect)` using `Projection.connection_lerp()`
- Draw straight connections as lines between entry/exit side centers
- Draw curved connections as arcs (can approximate with short line segments)
- Render the grid background (tile outlines)

#### 1b — Car Rendering
- Render each `Car` as a rectangle at its `TrackPosition`, rotated to match track direction
- Use `Projection.track_to_screen()` for position and rotation
- Render front/rear ends using `car.ends`

#### 1c — Manual Locomotive Controls
- Introduce `Locomotive` subclass of `Car` with throttle, brake, and direction controls
- Map keyboard input (arrow keys or WASD) in `Visualizer._update()`
- Throttle/brake apply forces; direction reverses velocity target

#### 1d — Switch State
- Add switch state (`normal` / `reversed`) to `Piece` for switch-type pieces
- Teach `TrackPosition.with_u()` to follow the active branch when traversing a switch
- Keyboard shortcut to toggle the switch under the locomotive

**Acceptance criteria**: You can drive a locomotive around a looped layout with a switch, see it move on screen, and throw the switch.

---

### Phase 2: Coupling

**Goal**: Cars couple into consists and can be assembled/disassembled.

#### 2a — Coupling Links
- Add `front_car: Car | None` and `rear_car: Car | None` to `Car`
- Add `couple(a, b)` / `uncouple(a)` operations with proximity and speed checks
- Add `consist_members` property walking the coupling chain

#### 2b — Constraint Propagation
- On each `update()`, enforce spring-like spacing between coupled cars
- Transmit impulse through consist when locomotive applies force
- Handle slack optionally (rigid first, slack as option later)

#### 2c — Consist Abstraction
- Introduce `Consist` (or computed property) grouping a coupled chain
- Route control inputs through consist to locomotive

**Acceptance criteria**: Locomotive can push into a car, couple, pull it around, and uncouple.

---

### Phase 3: Switching Gameplay

**Goal**: A minimal puzzle that requires correct railroad operations to solve.

#### 3a — Fixed Yard Layout
- Define a small yard layout (stub or hardcoded) with 1 locomotive, 2–3 cars, 1 switch
- Load it in `render_test.py`

#### 3b — Objective System
- Define a target car position (car X should end up on track Y)
- Detect win condition when cars reach targets
- Display status on screen

#### 3c — Polish
- Car labels / IDs on screen
- Track occupancy highlighting
- Simple HUD (throttle indicator, switch state)

**Acceptance criteria**: A human can pick up and run a switching puzzle from start to win condition.

---

### Phase 4: Layout Builder

**Goal**: Place and remove track tiles interactively.

#### 4a — Tile Editing
- Click to place/remove track pieces in `Visualizer`
- Support piece rotation before placement
- Connect pieces to neighbors automatically on placement

#### 4b — Piece Palette
- UI panel showing available piece types
- Click to select, then click on grid to place

#### 4c — Save / Load
- Serialize layout to JSON (grid positions + connection configs)
- Load from file on startup
- Auto-save on exit

**Acceptance criteria**: Build a custom layout, save it, reload it, and run trains on it.

---

### Phase 5: Tile World

**Goal**: Train activity visibly shapes the environment.

#### 5a — Tile Types
- Add `tile_type` to each grid cell (`grass`, `ballast`, `yard`, `town`, etc.)
- Render tiles with distinct colors/textures

#### 5b — Influence System
- Add per-tile influence floats (`traffic`, `ballast`, `vegetation`, `town`, `industry`)
- Each sim tick: diffuse values to neighbors, apply decay
- Trains emit `traffic` influence at their position

#### 5c — Tile Transitions
- Threshold rules: when influence crosses a value, change `tile_type`
- Example chain: `grass → ballast → dirty ballast → yard`
- Visible on screen

#### 5d — Seeds
- Stations emit `town` influence
- Industries emit `industry` influence
- Forests emit `vegetation` influence

**Acceptance criteria**: Run trains for a while, watch ballast form around active track, watch unused areas overgrow.

---

### Phase 6: Assisted Control and Planning

**Goal**: Automate basic railroad operations.

#### 6a — Assisted Primitives
- `drive_to(target_position)` — compute distance, apply force, stop at target
- `stop_at(target_position)` — precision stop
- `couple_to(car)` — drive toward car and couple
- `uncouple()` — uncouple at current position

#### 6b — Maneuver Library
- `pull_clear(consist, clear_point)` — move consist past a switch
- `runaround(locomotive, car)` — classic locomotive runaround maneuver
- `spot(car, target)` — deliver car to target industry

#### 6c — Task Planning
- Represent goals as DAGs of maneuver steps
- Execute a plan step-by-step
- Handle failures (car not reachable, path blocked)

#### 6d — Automated Switching Puzzle Solver
- Solver finds a plan for the current puzzle objective
- Executes plan via task planning layer
- Player can hand off to solver or do it manually

**Acceptance criteria**: Solver can automatically complete Phase 3 switching puzzles.

---

## Immediate Next Steps

The highest-priority items to unblock useful iteration:

1. **Render track** — implement `_render_piece` so the layout is visible
2. **Render cars** — show car positions on track
3. **Locomotive controls** — keyboard input for throttle/brake
4. **Switch state** — allow toggling switches during traversal
5. **Coupling** — push/pull cars

These five tasks form the core of Phase 1 and early Phase 2 and are enough to have a working, interactive toy railroad.
