from simulated_city.sheep_wolf_models import SheepSimulationParams, run_simulation


def test_simulation_is_deterministic_with_fixed_seed():
    params = SheepSimulationParams()

    first_run = run_simulation(params=params, ticks=20, seed=12345)
    second_run = run_simulation(params=params, ticks=20, seed=12345)

    first_values = [
        (
            summary.tick,
            summary.sheep_count,
            summary.grass_grown_cells,
            summary.births,
            summary.deaths,
            summary.sheep_ate_grass,
            round(summary.average_energy, 6),
        )
        for summary in first_run
    ]
    second_values = [
        (
            summary.tick,
            summary.sheep_count,
            summary.grass_grown_cells,
            summary.births,
            summary.deaths,
            summary.sheep_ate_grass,
            round(summary.average_energy, 6),
        )
        for summary in second_run
    ]

    assert first_values == second_values
