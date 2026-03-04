from simulated_city.config import load_config


def test_load_config_defaults_when_missing(tmp_path) -> None:
    """Test that default config loads when file is missing."""
    cfg = load_config(tmp_path / "missing.yaml")
    assert cfg.mqtt.host
    assert cfg.mqtt.port
    # Should have at least the default 'local' profile
    assert "local" in cfg.mqtt_configs or len(cfg.mqtt_configs) > 0


def test_load_config_reads_yaml(tmp_path) -> None:
    """Test reading YAML config with multi-broker structure."""
    p = tmp_path / "config.yaml"
    p.write_text(
        """
        mqtt:
          active_profiles: [default]
          profiles:
            default:
              host: example.com
              port: 1883
              tls: false
          client_id_prefix: demo
          keepalive_s: 30
        """.strip(),
        encoding="utf-8",
    )

    cfg = load_config(p)
    assert cfg.mqtt.host == "example.com"
    assert cfg.mqtt.port == 1883
    assert cfg.mqtt.tls is False
    assert cfg.mqtt.client_id_prefix == "demo"
    assert cfg.mqtt.keepalive_s == 30


def test_load_config_finds_parent_config_yaml(tmp_path, monkeypatch) -> None:
    """Test that config is found in parent directories."""
    # Simulate running from a subdirectory (like notebooks/)
    root = tmp_path
    (root / "config.yaml").write_text(
        """
        mqtt:
          active_profiles: [parent]
          profiles:
            parent:
              host: parent.example.com
              port: 1883
              tls: false
          client_id_prefix: demo
          keepalive_s: 30
        """.strip(),
        encoding="utf-8",
    )

    subdir = root / "notebooks"
    subdir.mkdir()
    monkeypatch.chdir(subdir)

    cfg = load_config("config.yaml")
    assert cfg.mqtt.host == "parent.example.com"

def test_load_config_multi_broker_with_active_profiles(tmp_path) -> None:
    """Test multi-broker configuration with active_profiles list."""
    p = tmp_path / "config.yaml"
    p.write_text(
        """
        mqtt:
          active_profiles: [local, public]
          profiles:
            local:
              host: localhost
              port: 1883
              tls: false
            public:
              host: broker.example.com
              port: 1883
              tls: false
          client_id_prefix: multi-test
          keepalive_s: 60
          base_topic: test-city
        """.strip(),
        encoding="utf-8",
    )

    cfg = load_config(p)
    
    # Primary broker (first in list)
    assert cfg.mqtt.host == "localhost"
    assert cfg.mqtt.port == 1883
    
    # All brokers available by name
    assert "local" in cfg.mqtt_configs
    assert "public" in cfg.mqtt_configs
    assert cfg.mqtt_configs["local"].host == "localhost"
    assert cfg.mqtt_configs["public"].host == "broker.example.com"


def test_load_config_single_broker_with_active_profiles(tmp_path) -> None:
    """Test single-broker configuration using active_profiles."""
    p = tmp_path / "config.yaml"
    p.write_text(
        """
        mqtt:
          active_profiles: [local]
          profiles:
            local:
              host: localhost
              port: 1883
              tls: false
          client_id_prefix: single-test
          keepalive_s: 60
          base_topic: test-city
        """.strip(),
        encoding="utf-8",
    )

    cfg = load_config(p)
    
    # Primary broker
    assert cfg.mqtt.host == "localhost"
    
    # Only local broker in configs
    assert "local" in cfg.mqtt_configs
    assert len(cfg.mqtt_configs) == 1


def test_load_config_reads_sheep_wolf_simulation_fields(tmp_path) -> None:
    """Test parsing Phase 2 sheep-wolf simulation config fields."""
    p = tmp_path / "config.yaml"
    p.write_text(
        """
mqtt:
  active_profiles: [local]
  profiles:
    local:
      host: localhost
      port: 1883
      tls: false

simulation:
  grid_width: 10
  grid_height: 10
  tick_interval_s: 0.5
  seed: 123
  initial_sheep: 30
  initial_wolves: 8
  initial_grass_coverage_pct: 70
  sheep_initial_energy: 8
  sheep_move_cost: 1
  sheep_eat_gain: 4
  sheep_reproduction_threshold: 10
  sheep_reproduction_probability: 0.08
  wolf_initial_energy: 12
  wolf_move_cost: 1
  wolf_eat_gain: 8
  wolf_reproduction_threshold: 14
  wolf_reproduction_probability: 0.04
  wolf_predation_capacity: 1
  grass_regrow_ticks: 5
  min_sheep_threshold: 12
  max_wolf_threshold: 25
  low_grass_threshold_pct: 25
  max_ticks: 1000
  extinction_grace_ticks: 20
        """.strip(),
        encoding="utf-8",
    )

    cfg = load_config(p)
    assert cfg.simulation is not None

    assert cfg.simulation.grid_width == 10
    assert cfg.simulation.grid_height == 10
    assert cfg.simulation.tick_interval_s == 0.5
    assert cfg.simulation.seed == 123
    assert cfg.simulation.initial_sheep == 30
    assert cfg.simulation.initial_wolves == 8
    assert cfg.simulation.initial_grass_coverage_pct == 70
    assert cfg.simulation.sheep_reproduction_probability == 0.08
    assert cfg.simulation.wolf_reproduction_probability == 0.04
    assert cfg.simulation.grass_regrow_ticks == 5
    assert cfg.simulation.max_ticks == 1000
    assert cfg.simulation.extinction_grace_ticks == 20


def test_load_config_sheep_wolf_simulation_defaults(tmp_path) -> None:
    """Test default values for omitted sheep-wolf simulation fields."""
    p = tmp_path / "config.yaml"
    p.write_text(
        """
mqtt:
  active_profiles: [local]
  profiles:
    local:
      host: localhost
      port: 1883
      tls: false

simulation: {}
        """.strip(),
        encoding="utf-8",
    )

    cfg = load_config(p)
    assert cfg.simulation is not None

    assert cfg.simulation.grid_width == 10
    assert cfg.simulation.grid_height == 10
    assert cfg.simulation.tick_interval_s == 0.5
    assert cfg.simulation.initial_sheep == 30
    assert cfg.simulation.initial_wolves == 8
    assert cfg.simulation.grass_regrow_ticks == 5
    assert cfg.simulation.max_ticks == 1000
    assert cfg.simulation.extinction_grace_ticks == 20