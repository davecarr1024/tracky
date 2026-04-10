# tracky

**tracky** is a virtual model railroad platform.

It combines a grid-based layout builder, a physically grounded train simulation, and a layered control system that can grow from manual driving to automated railroad operations.

At its core, tracky is about **making trains feel real to operate**—not just routing them, but handling them:
- pulling cuts of cars
- planning runarounds
- coupling and uncoupling
- working within the constraints of track, space, and momentum

On top of that, tracky explores the idea of a **living railroad world**:
- track and train movement shape the environment over time
- yards emerge where trains work heavily
- towns and industries grow around rail access
- unused areas decay and overgrow

The result is part toy, part simulation, part sandbox:
- build layouts like a model railroad with unlimited pieces
- solve switching puzzles and operational challenges
- experiment with railroad designs and watch them evolve

## Goals

- **Physical, not abstract**  
  Trains are heavy, directional machines with simple but believable motion.

- **Composable systems**  
  A small, clean simulation core supports multiple play styles: manual operation, puzzles, sandbox building, and automation.

- **Incremental complexity**  
  The project is designed to grow in layers:
  - start with manual control and simple switching
  - add layout building tools
  - introduce procedural world elements
  - build up automated train operation and planning

- **A platform, not just a game**  
  tracky is meant to be a foundation for experiments:
  - switching puzzles
  - layout generators
  - economic simulations
  - AI-driven operations

## Status

Early development. The current focus is a minimal vertical slice:

- a small yard layout
- one locomotive and a few cars
- manual controls (throttle, brake, direction)
- coupling and uncoupling
- a simple switching objective

From there, systems will be expanded incrementally.

## Design

See [design.md](./design.md) for a detailed breakdown of the architecture, systems, and roadmap.

## Philosophy

Build a small, working railroad first.  
Let complexity grow where the toy proves it’s fun.
