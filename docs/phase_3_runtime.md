# Phase 3 Runtime Documentation

This document validates Phase 3 (MQTT publishing from sheep agent) from [docs/implementationplan.md](docs/implementationplan.md).

## 1. What Was Created

### Files modified
- [notebooks/agent_sheep.ipynb](notebooks/agent_sheep.ipynb)
  - Added MQTT connection using `load_config()` + `MqttConnector`/`MqttPublisher`.
  - Added publishing per tick to tick/state/event topics.
  - Kept sheep-only local simulation logic from Phase 1.

### Files created
- [docs/phase_3_runtime.md](docs/phase_3_runtime.md)

### Library modules added
- None in Phase 3.

### `config.yaml` changes
- None in Phase 3.

## 2. How to Run

### Workflow A: Run sheep publisher notebook
1. Open [notebooks/agent_sheep.ipynb](notebooks/agent_sheep.ipynb).
2. Run Cell 1 (overview), then run Cell 2.
3. Observe output includes loaded config and MQTT topic names.
4. Run Cell 3.
5. Observe output line with chosen seed/tick/grid values.
6. Run Cell 4.
7. Observe per-tick rows with `| published` marker and final summary.
8. Run Cell 5.
9. Observe deterministic check and disconnect message.

### Workflow B: Verify message flow manually
1. Start a local MQTT monitor/client subscribed to `simulated-city/sim/#`.
2. Re-run Cell 4 in [notebooks/agent_sheep.ipynb](notebooks/agent_sheep.ipynb).
3. Confirm messages arrive on all three topics:
   - `simulated-city/sim/tick`
   - `simulated-city/sim/sheep/state`
   - `simulated-city/sim/events`

## 3. Expected Output

### Notebook outputs
- Cell 2 expected lines:
  - `Loaded config. Primary MQTT profile: <host>:<port>`
  - `MQTT connected: True` (or `False` if broker unavailable)
  - `Publish topics:` plus three topic lines.

- Cell 3 expected line:
  - `Using seed=<int>, ticks=30, grid=<w>x<h>`

- Cell 4 expected:
  - Header line: `tick sheep grass births deaths ate avg_energy`
  - One line per tick ending with `| published`
  - `Final summary:` followed by dictionary with keys:
    - `tick`
    - `sheep_count`
    - `grass_grown_cells`
    - `average_energy`

- Cell 5 expected:
  - `Deterministic run check: True`
  - `MQTT disconnected.`

### Failure interpretation
- If Cell 2 raises connection/TLS errors, MQTT broker credentials/network or TLS chain is incorrect.
- If Cell 4 runs but no external subscriber receives messages, verify broker/topic and subscription wildcard.
- If Cell 5 prints `False`, deterministic logic was changed unexpectedly.

## 4. MQTT Topics

### Published topics
- `simulated-city/sim/tick`
  - Publisher: sheep notebook
  - Payload JSON schema:
    - `tick` (int)
    - `seed` (int)
    - `timestamp_utc` (ISO-8601 string)

- `simulated-city/sim/sheep/state`
  - Publisher: sheep notebook
  - Payload JSON schema:
    - `tick` (int)
    - `seed` (int)
    - `sheep_count` (int)
    - `grass_grown_cells` (int)
    - `average_energy` (float)

- `simulated-city/sim/events`
  - Publisher: sheep notebook
  - Payload JSON schema:
    - `tick` (int)
    - `seed` (int)
    - `births` (int)
    - `deaths` (int)
    - `sheep_ate_grass` (int)

### Subscriptions in this phase
- None from sheep notebook (publish-only phase).

## 5. Debugging Guidance

### Common issues
- `ModuleNotFoundError` for `simulated_city`
  - Ensure editable install is active in the selected environment.

- `MQTT connected: False`
  - Check active profile in [config.yaml](config.yaml), broker availability, and credentials.

- TLS certificate verification failure
  - Use a broker/profile with valid cert chain locally, or test with local non-TLS profile for development.

### Practical checks
- Confirm base topic in config: `config.mqtt.base_topic`.
- Confirm topic subscription wildcard in monitor: `simulated-city/sim/#`.
- Re-run Cell 2 before Cell 4 if connection dropped.

## 6. Verification Commands

```bash
python scripts/verify_setup.py
python scripts/validate_structure.py
python -m pytest -q tests/test_config.py tests/test_sheep_wolf_core.py
```
