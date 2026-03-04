# Phase 2 Runtime Documentation

This document validates Phase 2 (Configuration Schema for Sheep-Wolf Simulation) from [docs/implementationplan.md](docs/implementationplan.md).

## 1. What Was Created

### Files modified
- [config.yaml](config.yaml)
  - Added top-level `simulation` section with sheep-wolf baseline parameters.
- [src/simulated_city/config.py](src/simulated_city/config.py)
  - Extended `SimulationConfig` with sheep-wolf fields.
  - Extended `_parse_simulation_config(...)` to parse new fields with defaults.
- [tests/test_config.py](tests/test_config.py)
  - Added tests for explicit sheep-wolf simulation parsing.
  - Added tests for simulation default fallback values.

### Notebooks/scripts created
- None in Phase 2.

### Library modules added to `src/simulated_city/`
- None new files (existing module extended).

### `config.yaml` changes summary
- Added keys under `simulation`:
  - grid/timing (`grid_width`, `grid_height`, `tick_interval_s`, `seed`)
  - initial populations (`initial_sheep`, `initial_wolves`, `initial_grass_coverage_pct`)
  - sheep parameters
  - wolf parameters
  - grass regrow parameters
  - control thresholds
  - stop condition (`max_ticks`, `extinction_grace_ticks`)

## 2. How to Run

### Workflow 1: Validate environment + structure
1. Open a terminal at repository root.
2. Run: `python scripts/verify_setup.py`
3. Observe environment verification success.
4. Run: `python scripts/validate_structure.py`
5. Observe structure checks complete (warnings may appear, but no blocking errors).

### Workflow 2: Validate Phase 2 config tests
1. In the same terminal, run: `python -m pytest -q tests/test_config.py`
2. Observe all `test_config.py` tests pass.
3. Confirm newly added sheep-wolf config tests are included in the pass count.

### Workflow 3: Manual config inspection
1. Open [config.yaml](config.yaml).
2. Confirm the top-level `simulation:` section exists.
3. Confirm key values exist (for example `grid_width: 10`, `initial_sheep: 30`, `max_ticks: 1000`).
4. Open [src/simulated_city/config.py](src/simulated_city/config.py).
5. Confirm `SimulationConfig` includes sheep-wolf fields and defaults.

## 3. Expected Output

### Command outputs
- `python scripts/verify_setup.py`
  - Expected: success message indicating required and notebook packages are present.

- `python scripts/validate_structure.py`
  - Expected: no blocking errors.
  - Optional warning: Phase 1 notebook has no MQTT connection (expected in Phase 1).

- `python -m pytest -q tests/test_config.py`
  - Expected summary includes all tests passing for config parsing.

### File-state expectations
- [config.yaml](config.yaml) contains a valid `simulation` mapping.
- [src/simulated_city/config.py](src/simulated_city/config.py) parses new fields without breaking older fields.
- [tests/test_config.py](tests/test_config.py) includes tests that:
  - assert explicit sheep-wolf values are read correctly
  - assert defaults are applied for missing fields

### Failure interpretation
- YAML parser errors in tests usually indicate indentation or malformed YAML fixture text.
- If `cfg.simulation is None` in new tests, the simulation section was not parsed correctly.
- If old config tests fail, backward compatibility may have regressed.

## 4. MQTT Topics (if applicable)

Phase 2 does not add MQTT publish/subscribe behavior.

- Topics published: none (Phase 2 scope)
- Topics subscribed: none (Phase 2 scope)
- Schema impact: only configuration readiness for future MQTT phases

## 5. Debugging Guidance

### Common issues and fixes
- `yaml.parser.ParserError` in config tests
  - Check indentation and top-level keys in YAML snippets (`mqtt:` and `simulation:` must align).

- Config fields parse as defaults unexpectedly
  - Confirm field names in YAML exactly match parser keys in `config.py`.

- Test fails on changed defaults
  - Update either expected values in tests or defaults in `SimulationConfig`, keeping plan consistency.

### Quick checks
- Run only config tests first:
  - `python -m pytest -q tests/test_config.py`
- Then run setup/structure checks to confirm repo constraints remain satisfied.

## 6. Verification Commands

```bash
python scripts/verify_setup.py
python scripts/validate_structure.py
python -m pytest -q tests/test_config.py
```
