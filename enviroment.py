# A* 1/sqrt(depth) + B* traffic_mean

import csv, random
from copy import deepcopy
import numpy as np

class RoadNetwork:

    def __init__(self, file_path, file_path_2):
        # Initialize the RoadNetwork with data from two CSV files.
        # The first file contains information about the road network.
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            first_line = next(csv_reader)
            max_nodes = int(first_line[0])
            # Initialize the network with maximum nodes and set initial values to infinity.
            self.network = (np.full((max_nodes, max_nodes, 2), float('inf'))).tolist()

            # Populate the network with edge weights from the CSV file.
            for row in csv_reader:
                self.network[int(row[0])][int(row[1])][0] = float(row[2])
                self.network[int(row[0])][int(row[1])][1] = 0  # Traffic initially set to 0
                
                self.network[int(row[1])][int(row[0])][0] = float(row[2])
                self.network[int(row[1])][int(row[0])][1] = 0

            # Set diagonal elements to 0 (distance from a node to itself).
            for i in range(max_nodes):
                self.network[i][i][0] = 0
            self.total_vertices = max_nodes

        # The second file contains information about drivers and their source-destination pairs.
        with open(file_path_2, 'r') as file:
            csv_reader = csv.reader(file)
            first_line = next(csv_reader)
            self.total_drivers = int(first_line[0])
            self.driver_src_dst = []
            for row in csv_reader:
                self.driver_src_dst.append([int(row[0]), int(row[1])])

        # Create a distance matrix from the network for shortest path calculations.
        self.dist = []
        for row in self.network:
            ls = []
            for val in row:
                ls.append(val[0])
            self.dist.append(ls)

        # Iterate through all vertices and find the shortest path using Floyd-Warshall algorithm.
        for k in range(self.total_vertices):
            for i in range(self.total_vertices):
                for j in range(self.total_vertices):
                    self.dist[i][j] = min(self.dist[i][j], self.dist[i][k] + self.dist[k][j])

# Example usage:
# road_network = RoadNetwork('network.csv', 'drivers.csv')
# # Access attributes like road_network.total_vertices, road_network.total_drivers, etc.

class State:
    
    def __init__(self, oldstate, net):
        # Initialize a State object.
        self.A = 34
        self.B = 122
        self.net = net
        self.network = deepcopy(self.net.network)
        self.oldstate = oldstate
        self.num_moves = 10

        if oldstate is None:
            # Initialize state for the first iteration.
            self.cur_locs = [driver_info[0] for driver_info in self.net.driver_src_dst] 
            self.depth = 0
            mask = ~np.isinf(np.array(self.network)[:,:,1])
            self.traffic_qual = 1 / (np.var(np.array(self.network)[:,:,1][mask]) + 1)
        else:
            # Update state based on the previous state.
            self.cur_locs = oldstate.cur_locs[:]
            self.depth = oldstate.depth + 1
            mask = ~np.isinf(np.array(self.network)[:,:,1])
            self.traffic_qual = oldstate.traffic_qual + 1 / (np.var(np.array(self.network)[:,:,1][mask]) + 1)
        self.best_poss = []

    def build(self):
        # Build the best possible moves for each driver based on neighbors.
        for i in range(self.net.total_drivers):
            src = self.cur_locs[i]
            src_neigh = []
            for j in range(len(self.net.network[src])):
                if self.net.network[src][j][0] != float('inf'):
                    src_neigh.append([self.net.dist[j][self.net.driver_src_dst[i][1]], j])
            src_neigh = sorted(src_neigh, key=lambda x: x[0])

            if len(src_neigh) == 2:
                src_neigh.append(src_neigh[0])
            elif len(src_neigh) == 1:
                src_neigh.append(src_neigh[0])
                src_neigh.append(src_neigh[0])
            src_neigh = src_neigh[:3]
            src_neigh = [row[1] for row in src_neigh]

            # Randomly select a move with a probability of 60%, else choose the best move.
            if random.uniform(0, 1) < 0.6:
                for x in range(3):
                    if self.net.dist[self.cur_locs[i]][self.net.driver_src_dst[i][1]] < \
                            self.net.dist[src_neigh[x]][self.net.driver_src_dst[i][1]]:
                        src_neigh[x] = src_neigh[0]
            self.best_poss.append(src_neigh)
            self.explored = set()

    def next_state(self):
        # Generate the next state based on random moves and exploration.
        next_st = None
        while next_st is None:
            l = []
            for i in range(self.net.total_drivers):
                val = random.randint(0, 9)
                if val < 5:
                    l.append(0)
                elif val < 8:
                    l.append(1)
                else:
                    l.append(2)
            l = tuple(l)
            if l not in self.explored:
                next_st = State(self, self.net)
                for i in range(self.net.total_drivers):
                    if self.cur_locs[i] != self.net.driver_src_dst[i]:
                        next_st.cur_locs[i] = self.best_poss[i][l[i]]
                        next_st.network[self.cur_locs[i]][next_st.cur_locs[i]][1] += 1
                    else:
                        next_st.cur_locs[i] = self.cur_locs[i]
                next_st.build()
                
        return next_st

    def reward(self):
        # Calculate the reward for the current state.
        return self.A * (1 / (self.depth * self.depth)) + self.B * (self.traffic_qual / self.depth)

    def terminal(self):
        # Check if the state is terminal (all drivers reached their destinations).
        for i in range(self.net.total_drivers):
            if self.net.driver_src_dst[i][1] != self.cur_locs[i]:
                return False
        return True
