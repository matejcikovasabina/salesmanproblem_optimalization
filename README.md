# Traveling Salesman Problem Solver

This project is a Python implementation of two optimization algorithms for solving a simplified version of the **Traveling Salesman Problem (TSP)**:

* Genetic Algorithm
* Simulated Annealing

The program randomly generates a set of cities on a 2D map and tries to find a short route that visits every city exactly once and returns back to the starting city.

The result is visualized using Matplotlib.

## Features

* Random generation of cities
* Solves the Traveling Salesman Problem using:

  * Genetic Algorithm
  * Simulated Annealing
* Supports two selection methods for the Genetic Algorithm:

  * Tournament selection
  * Roulette wheel selection
* Allows comparison between tournament and roulette selection
* Displays the best found path
* Shows how the path length changes during optimization
* Visualizes results using graphs

## Technologies Used

* Python
* Matplotlib
* Math module
* Random module

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

Install the required dependency:

```bash
pip install matplotlib
```

## Usage

Run the program:

```bash
python main.py
```

After running the program, choose which algorithm you want to use:

```text
1 - genetic algorithm
2 - simulated annealing
```

## Genetic Algorithm

If you choose:

```text
1 - genetic algorithm
```

you can then choose the selection method:

```text
1 - Tournament selection
2 - Roulette selection
3 - Both (compare tournament & roulette)
```

### Tournament Selection

Tournament selection randomly selects a small group of individuals from the population and chooses the best one as a parent.

In this project, the tournament size is:

```python
TOURNAMENT_SIZE = 3
```

### Roulette Wheel Selection

Roulette wheel selection chooses parents based on their fitness value. Individuals with better fitness have a higher chance of being selected.

## Simulated Annealing

If you choose:

```text
2 - simulated annealing
```

the program runs the simulated annealing algorithm.

Simulated annealing starts with a high temperature and gradually lowers it. Better solutions are always accepted, while worse solutions can sometimes be accepted depending on the current temperature.

This helps the algorithm avoid getting stuck in a local minimum.

## Configuration

The main configuration values are defined at the beginning of the file:

```python
WIDTH = 200
NUM_CITIES = 20
NUM_INDIVIDUALS = 50
NUM_GENERATION = 500
NUM_LIMIT = 50
MUTATION_RATE = 0.1
MIN_TEMPERATURE = 0.001
TEMPERATURE_RATE = 0.995
TEMPERATURE_START = 1000
TOURNAMENT_SIZE = 3
```

### Parameter Explanation

| Parameter           | Description                                               |
| ------------------- | --------------------------------------------------------- |
| `WIDTH`             | Size of the generated 2D map                              |
| `NUM_CITIES`        | Number of cities to generate                              |
| `NUM_INDIVIDUALS`   | Number of individuals in one genetic algorithm population |
| `NUM_GENERATION`    | Maximum number of generations in the genetic algorithm    |
| `NUM_LIMIT`         | Maximum number of generations without improvement         |
| `MUTATION_RATE`     | Probability of mutation in the genetic algorithm          |
| `MIN_TEMPERATURE`   | Minimum temperature for simulated annealing               |
| `TEMPERATURE_RATE`  | Rate at which the temperature decreases                   |
| `TEMPERATURE_START` | Starting temperature for simulated annealing              |
| `TOURNAMENT_SIZE`   | Number of individuals selected in tournament selection    |

## How the Genetic Algorithm Works

The genetic algorithm works with a population of possible paths.

Each path is represented as a list of city indexes. For example:

```python
[0, 4, 2, 1, 3]
```

The algorithm follows these steps:

1. Generate an initial random population.
2. Calculate the fitness of each path.
3. Select parents using tournament or roulette wheel selection.
4. Create new paths using crossover.
5. Randomly mutate some paths.
6. Keep the best individuals for the next generation.
7. Repeat until the maximum number of generations is reached or there is no improvement for a defined number of generations.

## Fitness Function

The fitness is calculated as:

```python
fitness = 1 / total_distance
```

This means that shorter paths have higher fitness.

The total distance is calculated using Euclidean distance between cities:

```python
sqrt((x1 - x2)^2 + (y1 - y2)^2)
```

## Mutation

Mutation is done by selecting two random positions in the path and reversing the part between them.

Example:

```python
[0, 1, 2, 3, 4]
```

If positions `1` and `4` are selected, the result can be:

```python
[0, 3, 2, 1, 4]
```

This helps create new variations of paths.

## Crossover

Crossover creates children from two parent paths.

The first half of the child comes from the first parent. The remaining cities are filled from the second parent while skipping cities that are already used.

This keeps every city in the path exactly once.

## How Simulated Annealing Works

Simulated annealing starts with a random path.

In each step:

1. A new candidate path is created using mutation.
2. The distance of the new path is calculated.
3. If the new path is shorter, it is accepted.
4. If the new path is longer, it may still be accepted with a certain probability.
5. The temperature is gradually decreased.
6. The process continues until the temperature reaches the minimum value.

The probability of accepting a worse solution is calculated as:

```python
probability = exp(-deltaE / temperature)
```

Where:

* `deltaE` is the difference between the new path length and the current path length
* `temperature` controls how likely the algorithm is to accept worse solutions

## Output

The program displays visual results using Matplotlib.

For the Genetic Algorithm, it shows:

* The best path found
* Path length over generations

When comparing tournament and roulette selection, it shows both methods side by side.

For Simulated Annealing, it shows:

* Path length during optimization
* Temperature decrease
* Best path found
