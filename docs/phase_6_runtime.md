# Phase 6 Runtime Notes

## Scope implemented
Phase 6 only: add a separate observer agent notebook and dashboard notebook for metrics visualization with a matrix view.

## Files created/modified
- Created: `notebooks/agent_observer.ipynb`
- Created: `notebooks/dashboard_observer.ipynb`
- Created: `docs/phase_6_runtime.md`
- Not modified: Phase 5 artifacts (`notebooks/agent_grass.ipynb`, `notebooks/agent_controller.ipynb`, `docs/phase_5_runtime.md`)

## What these notebooks do

### Observer agent
- Loads config via `simulated_city.config.load_config()`.
- Subscribes to:
  - `<base_topic>/sim/tick`
  - `<base_topic>/sim/sheep/state`
  - `<base_topic>/sim/wolf/state`
  - `<base_topic>/sim/grass/state`
  - `<base_topic>/sim/events`
  - `<base_topic>/sim/controller/commands`
- Publishes to:
  - `<base_topic>/sim/observer/metrics`
- Aggregates per-tick summaries for occupancy, population, energy, grass, and events.

### Dashboard observer
- Loads config via `simulated_city.config.load_config()`.
- Subscribes to:
  - `<base_topic>/sim/observer/metrics`
- Publishes start commands to:
  - `<base_topic>/sim/control/commands`
- Uses a live `matplotlib` matrix heatmap to show observer metrics at each tick.
- Renders textual per-tick summary (population, energy, grass, events, controller reason).
- Includes a **Start Simulation** button that sends `{ "command": "start" }` to begin the run.

## How to run
1. Start MQTT broker/profile from `config.yaml`.
2. Run all cells in notebooks in this order:
   - `notebooks/agent_sheep.ipynb`
   - `notebooks/agent_wolf.ipynb`
   - `notebooks/agent_grass.ipynb`
   - `notebooks/agent_controller.ipynb`
   - `notebooks/agent_observer.ipynb`
   - `notebooks/dashboard_observer.ipynb`
3. Keep the waiting/loop cells running in each agent notebook.
4. In `notebooks/dashboard_observer.ipynb`, run the subscription cell. It auto-renders when observer metrics arrive.
5. Click **Start Simulation** to send the start command.

## Expected output (notebook logs)

From observer notebook:

```text
Loaded config. Primary MQTT profile: localhost:1883
MQTT connected: True
Subscriptions active.
Observer agent loop running. Interrupt the cell to stop.
tick=1 sheep=30 wolves=8 grass=70.0% occupancy=0.38 events={'births': 0, 'deaths': 0, 'predation': 8, 'sheep_ate_grass': 6, 'wolf_births': 0, 'wolf_deaths': 0} command=baseline | published
```

From dashboard notebook:

```text
Loaded config. Primary MQTT profile: localhost:1883
MQTT connected: True
Subscribed topic target: city/sim/observer/metrics
Subscription active. Waiting for observer metrics...
Dashboard auto-render is active; no separate loop cell is required.
Received observer metrics message #1 (tick=1)
Rendered observer metrics message #1
```

## Expected output (example MQTT payload)

`.../sim/observer/metrics` example:

```json
{
  "tick": 12,
  "population": {
    "sheep": 27,
    "wolves": 9
  },
  "energy": {
    "sheep_average": 6.3
  },
  "grass": {
    "grown_cells": 64,
    "coverage_pct": 64.0
  },
  "events": {
    "births": 2,
    "deaths": 1,
    "predation": 8,
    "sheep_ate_grass": 5,
    "wolf_births": 1,
    "wolf_deaths": 0
  },
  "occupancy": {
    "estimated_ratio": 0.36,
    "grid_width": 10,
    "grid_height": 10,
    "method": "(sheep+wolves)/cells"
  },
  "controller": {
    "latest_reason": "baseline"
  },
  "timestamp_utc": "2026-03-04T12:00:00+00:00"
}
```

## Verification performed
- Phase 6 artifacts added without modifying Phase 5 code.
- Suggested focused checks:
  - `python scripts/verify_setup.py`
  - `python scripts/validate_structure.py`
  - `python -m pytest -q tests/test_config.py tests/test_sheep_wolf_core.py`

## Notes
- Occupancy is an estimate in this phase (`(sheep + wolves) / total_cells`) because per-cell occupancy messages are not yet published.
- Dashboard matrix view renders key metrics as a 3x3 heatmap with textual summaries per tick.
