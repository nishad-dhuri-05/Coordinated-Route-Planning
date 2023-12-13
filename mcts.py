import logging
import math 
import random
SCALAR = 2 / (2 * math.sqrt(2.0))
EXPAND_NODE = 0
class Node:
    def __init__(self, state, parent=None):
        # Initialize a Node with the given state and optional parent.
        self.visits = 1
        self.reward = 0.0
        self.state = state
        self.children = []  # List to store child nodes
        self.parent = parent  # Reference to the parent node

    def add_child(self, child_state):
        # Create a new child node with the given child_state and add it to the children list.
        child = Node(child_state, self)
        self.children.append(child)

    def update(self, reward):
        # Update the total reward and visit count of the node.
        self.reward += reward
        self.visits += 1

    def fully_expanded(self):
        # Check if the node is fully expanded, i.e., it has as many children as possible moves.
        if len(self.children) == self.state.num_moves:
            return True
        return False

    def __repr__(self):
        # Return a string representation of the node, including state, children count, visits, total reward,
        # and the exploit value (reward per visit).
        s = "Node: %s\n\tChildren: %d; visits: %d; reward: %f, exploit: %f" % (
            self.state,
            len(self.children),
            self.visits,
            self.reward,
            self.reward / self.visits,
        )
        return s
def uct_search(budget, root):
    # UCT (Upper Confidence Bound for Trees) search algorithm.
    for iteration in range(int(budget)):
        if iteration % 100 == 0:
            logging.debug("simulation: %d" % iteration)
            logging.debug(root)
        front = tree_policy(root)
        reward = default_policy(front.state)  # Perform default policy simulation
        backpropagation(front, reward)
        try:
            if best_child(root, 0).visits / budget > 0.5:
                # Break if a certain condition is met (e.g., a threshold on child visits).
                break
        except:
            logging.debug("No best child in iteration: %d" % iteration)
    return best_child(root, 0)


def default_policy(state):
    # Default policy for simulation: iteratively advance the state until a terminal state is reached.
    itr = 100
    while not state.terminal() and itr > 0:
        state = state.next_state()
        itr -= 1
    return state.reward()


def tree_policy(node):
    # Tree policy for node selection during the search.
    # A hack to force 'exploitation' in a game where there are many options,
    # and you may never/not want to fully expand first.
    while node and not node.state.terminal():
        if len(node.children) == 0:
            return expand(node)
        elif random.uniform(0, 1) < 0.6:
            node = best_child(node, SCALAR)
        else:
            if not node.fully_expanded():
                return expand(node)
            else:
                node = best_child(node, SCALAR)
    return node


def expand(node):
    # Expand the given node by adding a new child node with the next state.
    new_state = node.state.next_state()
    node.add_child(new_state)
    global EXPAND_NODE
    EXPAND_NODE += 1
    return node.children[-1]


def best_child(node, scalar):
    # Select the child node with the best UCT score.
    best_score = 0.0
    best_children = []
    for child in node.children:
        exploit = child.reward / child.visits
        explore = math.sqrt(2.0 * math.log(node.visits) / float(child.visits))
        score = exploit + scalar * explore
        if score == best_score:
            best_children.append(child)
        if score > best_score:
            best_children = [child]
            best_score = score
    if len(best_children) == 0:
        logging.warning("OOPS: no best child found, probably fatal")
        return None
    return random.choice(best_children)


def backpropagation(node, reward):
    # Backpropagate the reward information up the tree.
    while node is not None:
        node.visits += 1
        node.reward += reward
        node = node.parent
    return
