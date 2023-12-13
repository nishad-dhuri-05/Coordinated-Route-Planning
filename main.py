# Create a road network and initialize the first state.
import mcts
import enviroment
network = enviroment.RoadNetwork("input2_data.csv", "input2_driver.csv")
first_state = enviroment.State(None, network)
first_state.build()

# Create the root node for the search tree using the initial state.
root = mcts.Node(first_state)

val = 1
# Continue the search until the terminal condition is met (all drivers reach their destinations).
while not root.state.terminal():
    # Perform UCT search to find the best child node.
    child = mcts.uct_search(200, root)
    
    # Print the action number.
    print(f"Action {val}")
    print()

    # Print the moves for each driver from the current state to the next state.
    for i in range(network.total_drivers):
        print(f"Move Driver {i} from:{root.state.cur_locs[i]} to:{child.state.cur_locs[i]} ")
    print()
    print()

    # Update the root to the best child node for the next iteration.
    root = child
    val += 1
