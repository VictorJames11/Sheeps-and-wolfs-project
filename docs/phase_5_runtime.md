# Phase 5 Runtime Notes

## Scope implemented
Phase 5 only: add grass and controller agents that communicate over MQTT and publish grass state plus per-tick controller commands.

## Files created/modified
- Created: `notebooks/agent_grass.ipynb`
- Created: `notebooks/agent_controller.ipynb`
- Created: `docs/phase_5_runtime.md`
- Not modified: Phase 4 artifacts (`notebooks/agent_wolf.ipynb`, `docs/phase_4_runtime.md`)

## What these notebooks do

### Grass agent
- Loads config via `simulated_city.config.load_config()`.
- Connects with `MqttConnector` and publishes with `MqttPublisher`.
- Subscribes to:
  - `<base_topic>/sim/tick`
  - `<base_topic>/sim/events`
- Publishes to:
  - `<base_topic>/sim/grass/state`
- Uses binary grass regrowth state with regrow countdown (`grass_regrow_ticks`).

### Controller agent
- Loads config via `simulated_city.config.load_config()`.
- Subscribes to:
  - `<base_topic>/sim/tick`
  - `<base_topic>/sim/sheep/state`
  - `<base_topic>/sim/wolf/state`
  - `<base_topic>/sim/grass/state`
- Publishes to:
  - `<base_topic>/sim/controller/commands`
- Applies rule-based per-tick parameter updates.
- Evaluates hybrid stop condition (`max_ticks`, `extinction_grace_ticks`).

## How to run
1. Start MQTT broker/profile from `config.yaml`.
2. Run all cells in:
   - `notebooks/agent_sheep.ipynb`
   - `notebooks/agent_wolf.ipynb`
   - `notebooks/agent_grass.ipynb`
   - `notebooks/agent_controller.ipynb`
3. Observe publish logs from grass and controller notebooks each tick.

## Expected output (notebook logs)

These are example log lines. The numeric values are not guaranteed to be identical on every run.

What should match exactly:
- log format and keys (`tick`, `grass_grown`, `coverage`, `command`, `reason`)
- one grass publish per tick
- one controller command publish per tick

What can vary:
- `grass_grown` / `coverage` values (depends on incoming sheep event timing)
- controller `reason` and parameter values (depends on latest sheep/wolf/grass snapshot at tick time)

From grass notebook:

```text
Loaded config. Primary MQTT profile: localhost:1883
MQTT connected: True
Subscriptions active.
Grass agent loop running. Interrupt the cell to stop.
tick=1 grass_grown=68/100 coverage=68.0% | published
tick=2 grass_grown=65/100 coverage=65.0% | published
```

From controller notebook:

```text
Loaded config. Primary MQTT profile: localhost:1883
MQTT connected: True
Subscriptions active.
Controller agent loop running. Interrupt the cell to stop.
tick=1 command=UPDATE sheep_prob=0.08 wolf_prob=0.04 sheep_cost=1 wolf_cost=1 reason=['baseline'] | published
tick=2 command=UPDATE sheep_prob=0.04 wolf_prob=0.04 sheep_cost=2 wolf_cost=1 reason=['grass_low'] | published
```

## Reproducibility checklist (for closer match)
- Use one broker and one topic namespace only (single `base_topic`).
- Ensure `config.yaml` uses baseline values: `grid_width=10`, `grid_height=10`, `initial_grass_coverage_pct=70`, `seed=42`, `low_grass_threshold_pct=25`.
- Start notebooks in this order, then run the loop cell in each: sheep → wolf → grass → controller.
- Clear stale retained messages or use a fresh `base_topic` before rerunning.

## Expected output (example MQTT payloads)

`.../sim/grass/state` example:

```json
{
  "tick": 2,
  "seed": 2042,
  "grid_width": 10,
  "grid_height": 10,
  "grass_grown_cells": 65,
  "grass_coverage_pct": 65.0,
  "timestamp_utc": "2026-03-04T12:00:00+00:00"
}
```

`.../sim/controller/commands` example:

```json
{
  "tick": 2,
  "apply_next_tick": 3,
  "sheep_reproduction_probability": 0.04,
  "wolf_reproduction_probability": 0.04,
  "sheep_move_cost": 2,
  "wolf_move_cost": 1,
  "stop_requested": false,
  "reason": ["grass_low"],
  "snapshot": {
    "sheep_count": 26,
    "wolf_count": 8,
    "grass_coverage_pct": 20.0,
    "extinction_streak": 0
  },
  "timestamp_utc": "2026-03-04T12:00:00+00:00"
}
```

## Verification performed
- Phase 5 artifacts added without modifying Phase 4 code.
- Suggested focused checks:
  - `python scripts/verify_setup.py`
  - `python scripts/validate_structure.py`
  - `python -m pytest -q tests/test_config.py tests/test_sheep_wolf_core.py`

## Notes
- Phase 5 publishes controller commands each tick; full command-consumption by all agents can be expanded in a later phase if required.
- Topic shape remains per-agent and aligned with the approved concept and implementation plan.
