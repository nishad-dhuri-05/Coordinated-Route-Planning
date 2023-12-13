# Coordinated Route Planning (CRP) 

This repo presents a novel algorithm for coordinating large-scale routes, leveraging graph attention reinforcement learning and Monte Carlo Tree Search (MCTS).
It is dedicated for optimizing routes for an entire fleet of autonomous vehicles. The algorithm takes into consideration real-time traffic conditions and the overall traffic flow to efficiently plan routes.

## Overview

The primary goal of this project is to implement a coordinated route planning algorithm using a Monte Carlo Tree Search (MCTS) approach. The algorithm is designed to optimize routes for autonomous vehicles operating within a city environment, factoring in dynamic real-time traffic conditions.

## Problem Statement

Given a road network, denoted as a connected and directed
weighted graph G = (V, E), where V represents the set
of road intersections, E denotes the set of road segments,
W : E → R defines the edge weights indicating distances
between intersections, T : E → R signifies static traffic on
each road segment, and N(S, D) represents a set of drivers
with respective source (Si) and destination (Di) information,
the objective is to formulate a coordinated route planning
algorithm. This algorithm seeks to yield optimal routes for
all drivers, minimizing traffic congestion while accounting for
traffic conditions and minimizing the overall travel time


## Proposed Approach

 The road network is partitioned into regions, treating each as a player in
a Markov game. A bilevel optimization framework is employed,
with region planners coordinating route choices for vehicles
and a global planner (MCTS) evaluating the generated strategies. The
algorithm aims to balance user fairness and system efficiency,
address dimensionality challenges, and enhance route planning
by simulating traffic dynamics. (though the code is solely focussed on implementing MCTS as global planner)

## Repository Structure

---
    |
    |--datasets
    |       |
    |       |---input1_driver_data.csv
    |       |---input1_network_data.csv
    |       |---input2_driver_data.csv
    |       |---input2_network_data.csv  
    |       |---input3_driver_data.csv
    |       |---input3_network_data.csv  
    |       |---input4_driver_data.csv
    |       |---input4_network_data.csv  
    |       |---input5_driver_data.csv
    |       |---input5_network_data.csv     
    |
    |--city_network_data.csv
    |--driver_data.csv
    |--environment.py
    |--graph_plot.py
    |--main.py
    |--main.inpyb
    |--mcts.py
    |--readme.md
## Getting Started

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/CRP.git
   cd FleetRouteOptimizer

2. Place your input data in the datasets folder. Ensure the data is formatted in the required structure for driver_data.csv and network_data.csv.

3. Run the main script:
     ```bash
        python main.py


**Dataset Format**

*driver_data.csv*: Input data containing information about the drivers and their preferences.

*network_data.csv*: City network data that serves as the basis for route planning.



**Visualization**
To visualize the city network graph and the current locations of drivers, you can use the graph_plot.py file. Run the script:

```bash
        python graph_plot.py
```


## Contributing
To delve depper into proposed Approach, refer to the [term paper](./CoordinatedRoutePlanning_G15.pdf).

If you wish to contribute to this code, then implement necessary alterations to your forked version of this repo, and submit a merge request.
