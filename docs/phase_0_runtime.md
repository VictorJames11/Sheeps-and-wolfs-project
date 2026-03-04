# Phase 0 Runtime Documentation

This document validates Phase 0 (API Alignment and Plan Lock) from [docs/implementationplan.md](docs/implementationplan.md).

## 1. What Was Created

### Files modified
- [docs/concept.md](docs/concept.md)
  - Finalized MQTT topic decision to separate per-agent topics.
  - Finalized observer placement decision to separate observer notebook.

### Files created
- [docs/phase_0_runtime.md](docs/phase_0_runtime.md)

### Notebooks/scripts created
- None in Phase 0.

### Library modules added to `src/simulated_city/`
- None in Phase 0.

### `config.yaml` changes
- None in Phase 0.

## 2. How to Run

Phase 0 is documentation/API-alignment only (no simulation notebooks to run yet).

### Workflow A: Validate environment and repository structure
1. Open a terminal in the repository root.
2. Run: `python scripts/verify_setup.py`
3. Observe output confirming setup is valid.
4. Run: `python scripts/validate_structure.py`
5. Observe output confirming structure checks pass.
6. Run: `python -m pytest`
7. Observe test summary.

### Workflow B: Validate Phase 0 alignment decisions in docs
1. Open [docs/implementationplan.md](docs/implementationplan.md).
2. Read **Phase 0** section.
3. Confirm API lock states current class API (`MqttConnector`, `MqttPublisher.publish_json`).
4. Open [docs/concept.md](docs/concept.md).
5. Confirm section 2 says separate per-agent topic style is finalized.
6. Confirm section 4 says observer is a separate notebook (`notebooks/agent_observer.ipynb`).

## 3. Expected Output

### Command outputs
- Command: `python scripts/verify_setup.py`
  - Expected: script exits successfully with setup/verification success messaging.
  - Failure signal: non-zero exit code or missing dependency/conflict errors.

- Command: `python scripts/validate_structure.py`
  - Expected: script exits successfully with structure validation success messaging.
  - Failure signal: non-zero exit code with rule/structure violations.

- Command: `python -m pytest`
  - Expected: test session finishes with passing summary (or only pre-existing unrelated failures).
  - Failure signal: new failures introduced by Phase 0 docs-only changes (should be none).
  - Known external-case example: cloud MQTT TLS certificate verification can fail in some local environments without indicating a Phase 0 regression.

### Document checks
- In [docs/implementationplan.md](docs/implementationplan.md), Phase 0 includes:
  - `MqttConnector`
  - `MqttPublisher.publish_json`
  - separate per-agent topics
  - separate observer notebook

- In [docs/concept.md](docs/concept.md):
  - Section header is `## 2. MQTT Topics (Finalized)`.
  - A `Decision:` line explicitly states separate per-agent topics.
  - Notebook split section includes a `Decision:` line explicitly stating separate observer notebook.

If any of the above statements are missing, Phase 0 alignment is incomplete.

## 4. MQTT Topics (if applicable)

Phase 0 does not run live MQTT clients, but it finalizes topic architecture in documentation.

### Finalized topic set
- `city/sim/tick`
- `city/sim/sheep/state`
- `city/sim/wolf/state`
- `city/sim/grass/state`
- `city/sim/events`
- `city/sim/observer/metrics`
- `city/sim/controller/commands`

### Topic schema status
- Message schemas are not implemented in Phase 0.
- Schema details are defined in later implementation phases.

## 5. Debugging Guidance

### Common issues
- `python: command not found`
  - Ensure your virtual environment is activated.

- `verify_setup.py` fails on missing packages
  - Reinstall environment dependencies from project docs.

- `validate_structure.py` reports violations
  - Check docs/notebook structure against workshop constraints.

- `tests/test_mqtt_profiles.py` fails with TLS certificate verification errors
  - This can be environment/network/certificate-chain related for external brokers.
  - Re-run with valid trust chain/network access, or treat as external to Phase 0 docs-only changes.

### How to verify MQTT API lock quickly
- Open [src/simulated_city/mqtt.py](src/simulated_city/mqtt.py).
- Confirm class API exists:
  - `class MqttConnector`
  - `class MqttPublisher`
  - `publish_json(...)`

### What Phase 0 intentionally does not do
- No notebook execution.
- No MQTT runtime publish/subscribe flow.
- No simulation logic changes.

## 6. Verification Commands

```bash
python scripts/verify_setup.py
python scripts/validate_structure.py
python -m pytest
```
