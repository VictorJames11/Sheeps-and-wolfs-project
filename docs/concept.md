# Concept: Sheep and Wolves Simulated City

This document clarifies the project design before implementation.

## 1. Rewritten Components

### Trigger (system dynamics)
- The system evolves in discrete time steps (ticks) on a fixed 10×10 grid (100 cells).
- Mobile agents are sheep and wolves; both perform stochastic movement each tick.
- Sheep consume grass to gain energy; wolves consume sheep when co-located.
- Agents lose energy due to movement/metabolism, reproduce above a threshold, and die at zero energy.

### Observer (state measurement)
- Virtual sensors sample full-grid state every tick.
- Observations include occupancy, species counts, energy statistics, grass state, and event counts (predation, birth, death).

### Control Center (decision logic)
- A rule engine evaluates observed state against thresholds.
- It computes control actions (parameter adjustments) to keep populations and resources in target ranges.

### Response (actuation)
- Control outputs modify simulation parameters for the next tick (e.g., reproduction probabilities, regrowth rate, movement cost).
- The loop repeats: observe → evaluate → adjust → simulate next tick.

## 2. MQTT Topics (Finalized)

Suggested topic structure:
- `city/sim/tick`
- `city/sim/sheep/state`
- `city/sim/wolf/state`
- `city/sim/grass/state`
- `city/sim/events`
- `city/sim/observer/metrics`
- `city/sim/controller/commands`

Decision:
- Use separate per-agent topics (not one shared state topic).

## 3. Configuration Parameters

Minimum set:
- MQTT: host, port, username env var, password env var, TLS on/off, base topic, QoS.
- Simulation: grid width/height, tick interval, random seed, initial sheep/wolf counts.
- Energy: initial energy by species, move cost, eat gain, reproduction threshold, reproduction probability.
- Grass: regrowth delay/rate, max grass level (if continuous), binary vs continuous model.
- Control thresholds: min sheep, max wolves, low-grass trigger, hysteresis/cooldown.
- Geo/UI: map center lat/lon, zoom, coordinate mode (grid vs projected) if map visualization is used.

Note:
- GPS coordinates are optional if you keep the model purely as a logical grid.

## 4. Notebook Split (One Agent per Notebook)

Proposed notebooks:
- `notebooks/agent_sheep.ipynb`
- `notebooks/agent_wolf.ipynb`
- `notebooks/agent_grass.ipynb`
- `notebooks/agent_controller.ipynb`
- `notebooks/dashboard_observer.ipynb`

Decision:
- Use a separate observer notebook: `notebooks/agent_observer.ipynb`.

## 5. Classes vs Functions

Likely classes:
- Data models for agent state, cell state, event record, control command, config containers.
- Stateful runtime holders for sheep/wolf/grass behavior.

Likely functions:
- Movement step, energy update, predation check, reproduction check.
- Serialization/deserialization and topic naming helpers.

## 6. Library vs Notebook Responsibilities

Library (`src/simulated_city/`):
- Reusable config loading.
- MQTT connect/publish/subscribe helpers.
- Shared schemas/models.
- Validation and utility functions.

Notebooks:
- Agent loops (subscribe → update local state → publish).
- Dashboard and experiment-specific orchestration.

## 7. Finalized Simulation Decisions

1. Tick update order:
	- Move
	- Eat
	- Reproduce
	- Die
	- Regrow grass (end-of-tick environment update)

2. Cell occupancy:
	- Multi-occupancy is allowed (multiple sheep and wolves can share a cell).

3. Predation capacity:
	- Each wolf can consume at most 1 sheep per tick.

4. Reproduction timing:
	- Reproduction occurs after eating in the same tick.
	- Only agents still alive after eating can reproduce.
	- Energy gained from eating can count toward the reproduction threshold in that tick.

5. Grass model:
	- Binary grass state (`grown` / `not grown`).

6. Boundary behavior:
	- Wrap-around boundaries (torus).

7. Controller frequency:
	- Run control logic every tick.

8. Sensor model:
	- Perfect sensors (no delay/noise for baseline).

9. Reproducibility:
	- Use a fixed random seed for baseline runs.

10. Stop condition:
	- Hybrid stop condition.
	- Primary: fixed run length (e.g., `max_ticks = 1000`) for comparable experiments.
	- Early stop: terminate if either species is extinct (sheep = 0 or wolves = 0) for `extinction_grace_ticks` (e.g., 20) to avoid stopping on transient zero.


## 8. Suggested Starting Values (Draft)

For a beginner-stable run on 100 cells:
- Initial sheep: 30
- Initial wolves: 8
- Initial grass coverage: 70% grown
- Sheep move cost: 1
- Sheep eat gain: +4
- Wolf move cost: 1
- Wolf eat gain: +8
- Reproduction threshold: sheep 10, wolves 14
- Reproduction probability: sheep 0.08, wolves 0.04
- Grass regrowth: 5 ticks
- Tick interval: 0.5–1.0 s

These are initial defaults to tune during testing.
