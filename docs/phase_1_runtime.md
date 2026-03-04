# Phase 1 Runtime Documentation

This document validates Phase 1 (Minimal Single-Agent Grid Simulation, no MQTT) from [docs/implementationplan.md](docs/implementationplan.md).

## 1. What Was Created

### Notebooks/scripts created
- [notebooks/agent_sheep.ipynb](notebooks/agent_sheep.ipynb)

### Library modules added
- [src/simulated_city/sheep_wolf_models.py](src/simulated_city/sheep_wolf_models.py)

### Tests added
- [tests/test_sheep_wolf_core.py](tests/test_sheep_wolf_core.py)

### Configuration changes (`config.yaml`)
- None in Phase 1.
- Notebook reads existing config through `load_config()` and uses `simulation.seed` when available.

## 2. How to Run

### Workflow 1: Run the Phase 1 sheep simulation notebook
1. Open [notebooks/agent_sheep.ipynb](notebooks/agent_sheep.ipynb).
2. Run Cell 1 (markdown context), then run Cell 2 and Cell 3.
3. Observe Cell 2 output shows loaded config and primary MQTT profile.
4. Observe Cell 3 output shows seed, tick count, and grid size.
5. Run Cell 4.
6. Observe per-tick table and final summary dictionary.

### Workflow 2: Verify deterministic behavior in notebook
1. Keep [notebooks/agent_sheep.ipynb](notebooks/agent_sheep.ipynb) open.
2. Run Cell 5.
3. Observe output line `Deterministic run check: True`.
4. Re-run Cell 5.
5. Observe output remains `Deterministic run check: True`.

## 3. Expected Output

### Notebook expected outputs
- Cell 2 purpose: imports + config load
  - Expected line format:
    - `Loaded config. Primary MQTT profile: <host>:<port>`
  - Success means `load_config()` worked from notebook context.

- Cell 3 purpose: parameter and seed setup
  - Expected line format:
    - `Using seed=<int>, ticks=30, grid=10x10`
  - Success means run is reproducible and baseline params are set.

- Cell 4 purpose: run simulation
  - Expected first header line exactly:
    - `tick sheep grass births deaths ate avg_energy`
  - Expected a row per tick (30 rows by default).
  - Expected final block:
    - `Final summary:`
    - A dictionary including keys: `tick`, `sheep_count`, `grass_grown_cells`, `average_energy`.

- Cell 5 purpose: reproducibility check
  - Expected exact line:
    - `Deterministic run check: True`

### Failure interpretation
- If Cell 2 fails with import errors, environment or editable install is not active.
- If Cell 5 prints `False`, deterministic behavior regressed.
- If table is missing or malformed in Cell 4, simulation execution was interrupted.

## 4. MQTT Topics (if applicable)

Phase 1 does not publish or subscribe to MQTT.

- Topics published: none
- Topics subscribed: none
- Message schemas: none

MQTT integration starts in later phases.

## 5. Debugging Guidance

### Common errors and fixes
- `ModuleNotFoundError: No module named 'simulated_city'`
  - Activate the project virtual environment and ensure editable install is done.

- Notebook cannot find `config.yaml`
  - Run notebook from repository workspace and keep default `load_config()` path behavior.

- Determinism check fails
  - Confirm the same seed is used and no external random calls were inserted between runs.

### Increase visibility
- In Cell 4, lower `tick_count` to 10 for quick iteration while debugging.
- Add print statements around summary values in Cell 4 for step-by-step checks.

### Verify no MQTT usage in Phase 1
- Ensure notebook contains no `MqttConnector`, `MqttPublisher`, `connect`, `publish`, or topic strings.

## 6. Verification Commands

```bash
python scripts/verify_setup.py
python scripts/validate_structure.py
python -m pytest
```
