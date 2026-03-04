## Template for a project
Sheeps and Wolfs
### Step 1: Define Your Simulation (Before Any Code)
A simple ecological model, 100 cells at each simulation tick, so 10x10 grid, consisting of three agent types: wolves, sheep, and grass. The wolves and the sheep wander around the grid at random. Wolves and sheep both expend energy moving around, and replenish it by eating. Sheep eat grass, and wolves eat sheep if they end up on the same grid cell.

If wolves and sheep have enough energy, they reproduce, creating a new wolf or sheep (in this simplified model, only one parent is needed for reproduction). The grass on each cell regrows at a constant rate. If any wolves and sheep run out of energy, they die.

### My Smart City Project: [Project Name]

#### 1. The Trigger (Who/What is moving?)
The moving agents are sheep and wolves on a 2D grid.

Sheep move randomly to nearby cells, lose energy when moving, and gain energy by eating grass.
Wolves move randomly, lose energy when moving, and gain energy by eating sheep in the same cell.
Grass is part of the surroundings: it regrows over time and is consumed by sheep.
Time advances in simulation ticks; on each tick, agents move, eat, reproduce (if energy is high enough), or die (if energy reaches zero).*

#### 2. The Observer (What does the city see?)
The city uses virtual grid sensors that read the state of all 100 cells at each simulation tick, so 10x10 grid

Occupancy sensor: which cells contain sheep and wolves
Population sensor: total number of sheep and wolves
Energy sensor: average/min/max energy per species
Grass sensor: grass availability per cell (e.g., grown/not grown or level)
Event sensor: predation/reproduction/death events per tick
#### 3. The Control Center (The Logic)
It reads each tick’s sensor data (population, energy, grass, and events).
It compares values to configured thresholds (for example: minimum sheep count, maximum wolf count, low-grass limit).
If sheep are too low and wolves are high, it reduces wolf pressure (for example by lowering wolf reproduction probability).
If grass is too low, it slows sheep growth pressure (for example by reducing sheep reproduction probability).
If sheep are high and grass is healthy, it allows normal predator-prey dynamics.
It outputs control signals as parameter updates for the next tick, then repeats this loop continuously.

#### 4. The Response (What happens next?)
The controller is a rule-based parameter updater that applies the control center’s decisions to the next simulation tick.

It receives control signals from the logic layer each tick.
It updates simulation parameters, such as:
wolf reproduction probability
sheep reproduction probability
grass regrowth rate
optional movement energy cost
The updated parameters immediately affect agent behavior in the next tick.
This creates a continuous feedback loop: sense → decide → apply → repeat.