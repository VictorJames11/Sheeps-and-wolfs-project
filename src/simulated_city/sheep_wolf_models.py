from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True, slots=True)
class SheepSimulationParams:
    grid_width: int = 10
    grid_height: int = 10
    initial_sheep: int = 30
    initial_sheep_energy: int = 8
    sheep_move_cost: int = 1
    sheep_eat_gain: int = 4
    sheep_reproduction_threshold: int = 10
    sheep_reproduction_probability: float = 0.08
    grass_regrow_ticks: int = 5


@dataclass(slots=True)
class SheepAgent:
    x: int
    y: int
    energy: int


@dataclass(slots=True)
class TickSummary:
    tick: int
    sheep_count: int
    grass_grown_cells: int
    births: int
    deaths: int
    sheep_ate_grass: int
    average_energy: float


@dataclass(slots=True)
class SheepSimulationState:
    sheep: list[SheepAgent]
    grass_grown: list[list[bool]]
    grass_regrow_timer: list[list[int]]
    tick: int = 0


def create_initial_state(params: SheepSimulationParams, rng: random.Random) -> SheepSimulationState:
    sheep: list[SheepAgent] = []
    for _ in range(params.initial_sheep):
        sheep.append(
            SheepAgent(
                x=rng.randrange(params.grid_width),
                y=rng.randrange(params.grid_height),
                energy=params.initial_sheep_energy,
            )
        )

    grass_grown = [[True for _ in range(params.grid_width)] for _ in range(params.grid_height)]
    grass_regrow_timer = [[0 for _ in range(params.grid_width)] for _ in range(params.grid_height)]

    return SheepSimulationState(sheep=sheep, grass_grown=grass_grown, grass_regrow_timer=grass_regrow_timer)


def _move_sheep(agent: SheepAgent, params: SheepSimulationParams, rng: random.Random) -> None:
    dx, dy = rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
    agent.x = (agent.x + dx) % params.grid_width
    agent.y = (agent.y + dy) % params.grid_height


def _regrow_grass(state: SheepSimulationState, params: SheepSimulationParams) -> None:
    for row_index in range(params.grid_height):
        for col_index in range(params.grid_width):
            if not state.grass_grown[row_index][col_index] and state.grass_regrow_timer[row_index][col_index] > 0:
                state.grass_regrow_timer[row_index][col_index] -= 1
                if state.grass_regrow_timer[row_index][col_index] == 0:
                    state.grass_grown[row_index][col_index] = True


def step_simulation(
    state: SheepSimulationState,
    params: SheepSimulationParams,
    rng: random.Random,
) -> TickSummary:
    births = 0
    deaths = 0
    sheep_ate_grass = 0

    newborn_sheep: list[SheepAgent] = []
    surviving_sheep: list[SheepAgent] = []

    for agent in state.sheep:
        _move_sheep(agent, params, rng)

        agent.energy -= params.sheep_move_cost

        if state.grass_grown[agent.y][agent.x]:
            state.grass_grown[agent.y][agent.x] = False
            state.grass_regrow_timer[agent.y][agent.x] = params.grass_regrow_ticks
            agent.energy += params.sheep_eat_gain
            sheep_ate_grass += 1

        if (
            agent.energy >= params.sheep_reproduction_threshold
            and rng.random() < params.sheep_reproduction_probability
        ):
            child_energy = max(1, agent.energy // 2)
            agent.energy -= child_energy
            newborn_sheep.append(SheepAgent(x=agent.x, y=agent.y, energy=child_energy))
            births += 1

        if agent.energy <= 0:
            deaths += 1
        else:
            surviving_sheep.append(agent)

    state.sheep = surviving_sheep + newborn_sheep

    _regrow_grass(state, params)

    state.tick += 1

    sheep_count = len(state.sheep)
    total_energy = sum(agent.energy for agent in state.sheep)
    average_energy = (total_energy / sheep_count) if sheep_count > 0 else 0.0
    grass_grown_cells = sum(1 for row in state.grass_grown for cell in row if cell)

    return TickSummary(
        tick=state.tick,
        sheep_count=sheep_count,
        grass_grown_cells=grass_grown_cells,
        births=births,
        deaths=deaths,
        sheep_ate_grass=sheep_ate_grass,
        average_energy=average_energy,
    )


def run_simulation(
    params: SheepSimulationParams,
    ticks: int,
    seed: int,
) -> list[TickSummary]:
    rng = random.Random(seed)
    state = create_initial_state(params, rng)

    summaries: list[TickSummary] = []
    for _ in range(ticks):
        summaries.append(step_simulation(state, params, rng))
    return summaries
