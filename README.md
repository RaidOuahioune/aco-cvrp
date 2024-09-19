# CVPR: Capacitated Vehicle Routing Problem using Ant Colony Optimization (ACO)

## Overview

This Python code solves the **Capacitated Vehicle Routing Problem (CVRP)** using an **Ant Colony Optimization (ACO)** algorithm. The problem involves determining the optimal routes for a fleet of vehicles to service a set of customers with demands, starting and ending at a depot, without exceeding vehicle capacity.

## Problem Definition

The **Capacitated Vehicle Routing Problem (CVRP)** can be described as follows:

- **Graph**: A complete graph $G = (V, E)$, where $V = \{0, 1, \dots, n\}$ is the set of nodes, with node 0 being the depot, and $E$ is the set of edges between the nodes.
- **Demand**: Each customer node $i \in V \setminus \{0\}$ has a demand $d_i$.
- **Vehicles**: There are $m$ vehicles, each with a capacity $C$.
- **Objective**: Minimize the total distance traveled by all vehicles while ensuring that each customer is visited exactly once, and the total demand serviced by each vehicle does not exceed its capacity.

## Ant Colony Optimization (ACO) Algorithm

### Pheromone and Heuristic Information

The ACO algorithm mimics the behavior of ants searching for food. The **pheromone matrix** $\tau_{ij}$ stores the pheromone values on the path from node $i$ to node $j$, guiding the ants in their path construction. Over time, pheromones **evaporate**, and paths that are more optimal receive more pheromone reinforcement.

The probability of moving from node $i$ to node $j$ is determined by a combination of the pheromone trail $\tau_{ij}$ and a heuristic value $\eta_{ij} = \frac{1}{d_{ij}}$, where $d_{ij}$ is the distance between nodes $i$ and $j$. The transition probability $p_{ij}$ is calculated as:

$p_{ij} = \frac{(\tau_{ij})^\alpha (\eta_{ij})^\beta}{\sum_{k \in N} (\tau_{ik})^\alpha (\eta_{ik})^\beta}$



Where:
- $\alpha$ controls the influence of pheromone values.
- $\beta$ controls the influence of heuristic values.
- $N$ is the set of unvisited nodes.

### Ants’ Path Construction

Each ant starts at the depot (node 0) and constructs a path by probabilistically selecting the next node based on the transition probabilities. This process continues until all nodes have been visited. Each ant’s path is evaluated by its total length, and the global best path is updated if a shorter one is found.

### Pheromone Update

After each iteration, the pheromone matrix is updated. Pheromone values are **evaporated** globally by multiplying each value by an evaporation factor $\rho$. Then, additional pheromone is deposited on the paths taken by the ants, with more pheromone added to shorter paths. The pheromone update formula is:


$\tau_{ij} = (1 - \rho) \cdot \tau_{ij} + \sum_{k} \Delta \tau_{ij}^k$

Where $\Delta \tau_{ij}^k$ is the pheromone deposited by the $k$-th ant, calculated as:


$\Delta \tau_{ij}^k = \frac{Q}{L_k}$


Where:
- $Q$ is a constant.
- $L_k$ is the total length of the $k$-th ant's path.
