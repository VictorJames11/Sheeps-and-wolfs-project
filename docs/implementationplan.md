## Plan: Sheep-Wolf Distributed Simulation Implementation

This plan implements your approved design from [docs/concept.md](docs/concept.md) in small, testable phases that match the workshop constraints: one agent per notebook, MQTT communication between notebooks, configuration loaded from [config.yaml](config.yaml), and anymap-ts visualization.
You chose these key decisions: separate per-agent topics, separate observer notebook, fixed tick order, binary grass, torus boundary, controller every tick, perfect sensors, fixed seed, and hybrid stop condition.
A short Phase 0 is included to align MQTT API naming before implementation so later phases stay consistent and low-risk.

### Phase 0: API Alignment and Plan Lock
**Goal:** Freeze interfaces and remove naming drift before building notebooks.

**New Files:**
- Modify [docs/implementationplan.md](docs/implementationplan.md) (this file)
- Reference [src/simulated_city/mqtt.py](src/simulated_city/mqtt.py), [src/simulated_city/config.py](src/simulated_city/config.py), [docs/concept.md](docs/concept.md)

**Implementation Details:**
- Lock plan to current MQTT class API (`MqttConnector`, `MqttPublisher.publish_json`) unless wrappers are added later.
- Lock topic style to separate per-agent topics.
- Lock observer as separate notebook (not dashboard-only observer).

**Dependencies:**
- None.

**Verification:**
- Manual: confirm all later phases reference the same MQTT API and topic pattern.
- Run: `python scripts/verify_setup.py`

**Investigation:**
- Understand current `mqtt.py` public API and avoid introducing conflicting function names in notebooks.

---

### Phase 1: Minimal Single-Agent Grid Simulation (No MQTT)
**Goal:** Prove core sheep-grid dynamics with fixed tick order and deterministic baseline.

**New Files:**
- Create notebook: [notebooks/agent_sheep.ipynb](notebooks/agent_sheep.ipynb)
- Optional helper module: [src/simulated_city/sheep_wolf_models.py](src/simulated_city/sheep_wolf_models.py)
- Optional tests: [tests/test_sheep_wolf_core.py](tests/test_sheep_wolf_core.py)

**Implementation Details:**
- Implement 10x10 grid, sheep movement, energy update, binary grass consume/regrow.
- Enforce tick order: move → eat → reproduce → die → regrow grass.
- Use fixed seed from config placeholder/default for reproducibility.
- No MQTT yet; local loop and printed tick summaries only.

**Dependencies:**
- None beyond existing project deps.

**Verification:**
- Run: `python -m pytest`
- Manual: open notebook, run all cells, confirm deterministic repeated run behavior.

**Investigation:**
- Confirm baseline parameter stability and whether sheep-only dynamics are reasonable before adding predators.

---

### Phase 2: Configuration Schema for Sheep-Wolf Simulation
**Goal:** Move all simulation and controller parameters into config with load-time validation.

**New Files:**
- Modify [config.yaml](config.yaml)
- Modify [src/simulated_city/config.py](src/simulated_city/config.py)
- Modify [tests/test_config.py](tests/test_config.py)

**Implementation Details:**
- Add sheep-wolf simulation section: grid size, tick interval, seed, energy/reproduction parameters, grass regrow ticks.
- Add controller thresholds and stop-condition fields (`max_ticks`, `extinction_grace_ticks`).
- Keep MQTT profile settings centralized and reused by all notebooks via `load_config()`.

**Dependencies:**
- None.

**Verification:**
- Run: `python scripts/verify_setup.py`
- Run: `python -m pytest`
- Manual: load config from notebook directory and confirm parent-path discovery still works.

**Investigation:**
- Ensure new schema extensions do not break existing template tests or non-simulation uses.

---

### Phase 3: MQTT Publishing from Sheep Agent
**Goal:** Turn the single agent into a publisher of state/events topics.

**New Files:**
- Modify [notebooks/agent_sheep.ipynb](notebooks/agent_sheep.ipynb)
- Optional shared topic/schema helper: [src/simulated_city/sheep_wolf_topics.py](src/simulated_city/sheep_wolf_topics.py)
- Optional tests: [tests/test_mqtt_profiles.py](tests/test_mqtt_profiles.py)

**Implementation Details:**
- Connect using `load_config()` + current MQTT helper classes.
- Publish to:
  - `city/sim/tick`
  - `city/sim/sheep/state`
  - `city/sim/events`
- Include consistent payload shape with tick index and seed metadata.

**Dependencies:**
- None.

**Verification:**
- Run: `python scripts/verify_setup.py`
- Manual: run sheep notebook and verify publish logs each tick.

**Investigation:**
- Confirm message cadence and payload size are stable at chosen tick interval.

---

### Phase 4: Add Wolf Agent with MQTT Subscription
**Goal:** Enable predator-prey interaction through MQTT message flow.

**New Files:**
- Create [notebooks/agent_wolf.ipynb](notebooks/agent_wolf.ipynb)
- Modify [notebooks/agent_sheep.ipynb](notebooks/agent_sheep.ipynb) if schema coordination is needed
- Optional shared state utilities: [src/simulated_city/sheep_wolf_state.py](src/simulated_city/sheep_wolf_state.py)

**Implementation Details:**
- Wolf subscribes to sheep state/tick topics and publishes:
  - `city/sim/wolf/state`
  - `city/sim/events`
- Enforce predation cap: max 1 sheep per wolf per tick.
- Keep multi-occupancy semantics and torus movement consistent.

**Dependencies:**
- None.

**Verification:**
- Manual: run sheep and wolf notebooks in parallel; confirm both publish and consume expected topics.
- Run: `python -m pytest`

**Investigation:**
- Validate ordering assumptions under distributed timing and decide how to handle late messages.

---

### Phase 5: Grass and Controller Agents
**Goal:** Complete closed-loop control with environment and policy adjustments.

**New Files:**
- Create [notebooks/agent_grass.ipynb](notebooks/agent_grass.ipynb)
- Create [notebooks/agent_controller.ipynb](notebooks/agent_controller.ipynb)

**Implementation Details:**
- Grass agent manages binary regrowth and publishes:
  - `city/sim/grass/state`
- Controller subscribes to sheep/wolf/grass/events and publishes:
  - `city/sim/controller/commands`
- Apply every-tick control updates to reproduction/energy-cost parameters.
- Respect hybrid stop condition from config.

**Dependencies:**
- None.

**Verification:**
- Manual: run sheep, wolf, grass, controller together; verify command topic influences next-tick behavior.
- Run: `python -m pytest`

**Investigation:**
- Tune threshold values to avoid unstable oscillations or immediate collapse.

---

### Phase 6: Observer + Dashboard Visualization (anymap-ts)
**Goal:** Provide observable system health and spatial view with separate observer notebook.

**New Files:**
- Create [notebooks/agent_observer.ipynb](notebooks/agent_observer.ipynb)
- Create [notebooks/dashboard_observer.ipynb](notebooks/dashboard_observer.ipynb)

**Implementation Details:**
- Observer subscribes to all state/event topics and publishes:
  - `city/sim/observer/metrics`
- Dashboard subscribes to observer metrics and renders with anymap-ts.
- Show occupancy/population/energy/grass/events summaries per tick.

**Dependencies:**
- None (anymap-ts already in notebook extras).

**Verification:**
- Manual: run all agent notebooks + observer + dashboard, confirm live updates and map refresh.
- Run: `python scripts/verify_setup.py`

**Investigation:**
- Decide final visualization density (cell heatmap vs markers) for readability at 10x10.

---

### Phase 7: Hardening, Documentation, and Validation
**Goal:** Make the workshop implementation reproducible and review-ready.

**New Files:**
- Update [docs/exercises.md](docs/exercises.md)
- Update [docs/mqtt.md](docs/mqtt.md)
- Update [docs/setup.md](docs/setup.md) if run workflow changed
- Add/adjust tests in [tests](tests)

**Implementation Details:**
- Document startup order for distributed notebooks.
- Document topic schemas and expected message examples.
- Add sanity tests for config parsing and helper utilities.
- Include PR line: `Docs updated: yes/no`.

**Dependencies:**
- None.

**Verification:**
- Run: `python scripts/verify_setup.py`
- Run: `python scripts/validate_structure.py`
- Run: `python -m pytest`
- Manual: end-to-end notebook run from clean environment.

**Investigation:**
- Identify the minimum subset for classroom demo vs full experiment mode.

---

## Global Verification Checklist
- Install path: `python -m pip install -e ".[dev,notebooks]"`
- Validation: `python scripts/verify_setup.py`
- Structure checks: `python scripts/validate_structure.py`
- Tests: `python -m pytest`
- Manual: run all notebooks in distributed order and confirm MQTT/topic flow.

---

## Decisions Captured
- Concept source: [docs/concept.md](docs/concept.md)
- MQTT API direction: current class API in [src/simulated_city/mqtt.py](src/simulated_city/mqtt.py)
- Topic style: separate per-agent topics
- Observer placement: separate observer notebook
- Finalized simulation rules: section 7 in [docs/concept.md](docs/concept.md)
