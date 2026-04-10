# CLAUDE.md — tracky

## Project Overview

tracky is a virtual model railroad platform in Python 3.13. It simulates physically-grounded train movement on a grid-based layout, with a layered control system that grows from manual driving toward automated operations. There is also a procedural tile-world system where train activity shapes the environment over time.

The project is in early development. The simulation core (track graph, car physics, projection math) is well-established. The rendering, coupling, switching control, tile world, and control layers are not yet implemented.

## Commands

```bash
poetry run poe format      # black formatting (100-char lines)
poetry run poe lint        # ruff linting
poetry run poe typecheck   # pyright strict type checking
poetry run poe test        # pytest with coverage
poetry run poe all         # format + lint + typecheck + test
poetry run poe render_test # run the pygame visualizer
```

All code must pass `poe all` cleanly. Type annotations are required everywhere; pyright is run in strict mode.

## Architecture

```
tracky/
  core/         Error, Errorable, Validatable — base mixins
  track/
    grid/       Position, Direction, Rotation, Grid — 2D tile map
    pieces/     Connection, Piece, Position — track graph
  cars/         Car, CarManager — physics and collections
  sim/          Sim — top-level orchestrator
  visuals/      screen-space math, Projection, Visualizer
scripts/        render_test.py — visualization entry point
docs/           design.md, roadmap.md
```

## Key Patterns

### Validatable / bidirectional relationships
`Validatable` (in `core/validatable.py`) provides an invariant-checking framework. Classes that hold bidirectional references (Grid ↔ Piece, Piece ↔ Connection, Car ↔ CarManager) use `_pause_validation()` context managers to batch mutations before validation runs. Always use `_pause_validation()` when making multi-step relational changes.

### Errorable
`Errorable` (in `core/errorable.py`) provides `_error()` and `_try()` helpers for creating typed, context-rich exceptions. Prefer these over bare `raise ValueError(...)`.

### Track navigation
Track positions are represented as `(connection, u)` where `u ∈ [0, 1)` is the parameter along a connection. The `TrackPosition.with_u()` method handles transitions between connections and pieces automatically. Extending traversal logic should go through this interface.

### Projection
`Projection` (in `visuals/projection.py`) converts between grid coordinates and screen pixels. It handles both straight and curved connections, returning `(screen_position, rotation)` pairs for rendering. This is the bridge between the simulation and the visualizer.

## Code Conventions

- All public attributes are typed properties or `@dataclass` fields
- No bare `Optional` — use `X | None` with explicit `None` checks
- Frozen dataclasses for value types (`Position`, `Offset`, `Rotation`, etc.)
- Mutable classes inherit from `Validatable` and use `_pause_validation()`
- Tests live alongside source files (`foo_test.py` next to `foo.py`)
- `visualizer.py` and `scripts/` are excluded from coverage (marked `# coverage: skip file`)
- Line length: 100 characters

## Current State

See `docs/roadmap.md` for a detailed assessment and plan.

**What works:**
- Track graph (Grid, Piece, Connection) with arbitrary topologies
- Track-space navigation (TrackPosition with seamless piece transitions)
- Car physics (position, velocity, mass, damping, force/impulse)
- CarManager batch updates
- Sim orchestration
- Full screen-space math and projection (including curved connections)
- Comprehensive test suite (pyright strict, 60+ tests)

**Not yet implemented:**
- Rendering (visualizer._render_piece is a stub)
- Coupling model
- Switch state and control
- Locomotive / throttle controls
- Tile world and influence system
- All control layers above manual

## Testing

Tests use `pytest` with `pytest-subtests` for parameterized cases. Use `with subtests.test(...)` for parameterized table-driven tests. Use `pytest.approx()` for floating-point comparisons.

Focus tests on invariants and scenario correctness. Avoid excessive micro-tests for trivial getters. Do not mock internal collaborators — use real objects.

## Design Reference

See `docs/design.md` for the full architecture, system descriptions, and open questions.
See `docs/roadmap.md` for the current-state assessment and phased implementation plan.
