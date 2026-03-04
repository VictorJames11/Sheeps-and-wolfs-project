# Phase 4 Runtime Notes

## Scope implemented
Phase 4 only: add a wolf agent notebook that subscribes to sheep/tick topics and publishes wolf state plus wolf events.

## Files created/modified
- Created: `notebooks/agent_wolf.ipynb`
- Created: `docs/phase_4_runtime.md`
- Not modified: Phase 3 sheep publisher notebook (`notebooks/agent_sheep.ipynb`)

## What the wolf notebook does
- Loads config via `simulated_city.config.load_config()`.
- Connects to MQTT with `MqttConnector` and publishes using `MqttPublisher`.
- Subscribes to:
  - `<base_topic>/sim/sheep/state`
  - `<base_topic>/sim/tick`
- Publishes to:
  - `<base_topic>/sim/wolf/state`
  - `<base_topic>/sim/events`
- Enforces predation cap logic as configured (`wolf_predation_capacity`, default 1).

## Runtime behavior
- On sheep-state messages, caches latest `sheep_count`.
- On tick messages, computes:
  - estimated predation (`min(wolf_count * capacity, sheep_count)`)
  - small stochastic wolf births/deaths using fixed seed offset
- Publishes one wolf-state payload and one wolf event payload per tick.

## How to run
1. Start MQTT broker/profile from `config.yaml`.
2. Run all cells in `notebooks/agent_sheep.ipynb` (Phase 3 publisher).
3. Run all cells in `notebooks/agent_wolf.ipynb`.
4. Observe per-tick wolf publish logs in the wolf notebook output.

## Expected topic payload keys
- `.../sim/wolf/state`:
  - `tick`, `seed`, `wolf_count`, `predation_capacity`, `estimated_predation`, `timestamp_utc`
- `.../sim/events` (from wolf):
  - `tick`, `seed`, `source`, `wolf_births`, `wolf_deaths`, `estimated_predation`

## Expected output (notebook logs)
When `agent_sheep.ipynb` and `agent_wolf.ipynb` both run, you should see lines like:

```text
Loaded config. Primary MQTT profile: localhost:1883
MQTT connected: True
Subscriptions active.
Wolf agent loop running. Interrupt the cell to stop.
tick=1 sheep=30 wolves=8 predation=8 births=0 deaths=0 | published
tick=2 sheep=29 wolves=8 predation=8 births=0 deaths=0 | published
tick=3 sheep=27 wolves=9 predation=8 births=1 deaths=0 | published
```

Expected behavior:
- One wolf-state publish per tick
- One wolf event publish per tick
- `estimated_predation` never exceeds `wolf_count * predation_capacity`
- `estimated_predation` never exceeds latest known sheep count

## Expected output (example MQTT payloads)

`.../sim/wolf/state` example:

```json
{
  "tick": 3,
  "seed": 1042,
  "wolf_count": 9,
  "predation_capacity": 1,
  "estimated_predation": 8,
  "timestamp_utc": "2026-03-04T12:00:00+00:00"
}
```

`.../sim/events` (wolf) example:

```json
{
  "tick": 3,
  "seed": 1042,
  "source": "wolf",
  "wolf_births": 1,
  "wolf_deaths": 0,
  "estimated_predation": 8
}
```

## Verification performed
- Phase 4 implementation added without changing Phase 3 code.
- Suggested focused checks:
  - `python scripts/verify_setup.py`
  - `python scripts/validate_structure.py`
  - `python -m pytest -q tests/test_config.py tests/test_sheep_wolf_core.py`

## Notes
- This phase intentionally keeps distributed timing simple; it uses latest known sheep state when a tick arrives.
- Handling of delayed/out-of-order messages is deferred to a later phase investigation per the approved plan.
