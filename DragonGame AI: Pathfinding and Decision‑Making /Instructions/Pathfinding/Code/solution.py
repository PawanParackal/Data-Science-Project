from game_env import GameEnv
from game_state import GameState
import heapq
import math

"""
solution.py

This file is a template you should use to implement your solution.

You should implement each of the method stubs below. You may add additional methods and/or classes to this file if you 
wish. You may also create additional source files and import to this file if you wish.

COMP3702 Assignment 1 "Dragon Game" Support Code

Last updated by njc 07/08/23
"""

class Node:

    def __init__(self, state, cost=0, action=None, parent=None, heuristic=0):
        self.state = state
        self.cost = cost
        self.action = action
        self.parent = parent
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

class Solver:

    def __init__(self, game_env):
        self.game_env = game_env
        self.heuristic_cache = {}  # Cache for computed heuristic values
        self.preprocess_heuristic()  # Preprocess the heuristic once during initialization

        #
        #
        # TODO: Define any class instance variables you require here (avoid performing any computationally expensive
        #  heuristic preprocessing operations here - use the preprocess_heuristic method below for this purpose).
        #
        #

    # === Uniform Cost Search ==========================================================================================
    def search_ucs(self):
        """
        Find a path which solves the environment using Uniform Cost Search (UCS).
        :return: path (list of actions, where each action is an element of GameEnv.ACTIONS)
        """

        #
        #
        # TODO: Implement your UCS code here.
        #
        #

        start_state = self.game_env.get_init_state()

        if self.game_env.is_solved(start_state):
            return []

        heap = [Node(start_state)]
        explored = {}
        nodes_expanded = 0

        while heap:
            nodes_expanded += 1
            print("Nodes expanded:", nodes_expanded)                                                                                                                                                                                                                                                                                                               
            nodes_on_fringe = len(heap)  # Get the number of nodes on the fringe when the search terminates
            print("Nodes on fringe:", nodes_on_fringe)
            node = heapq.heappop(heap)
            current_state = node.state

            if current_state in explored and node.cost >= explored[current_state]:
                continue
            explored[current_state] = node.cost

            if self.game_env.is_solved(current_state):
                return self.reconstruct_path(node)

            for action in self.game_env.ACTIONS:
                success, next_state = self.game_env.perform_action(current_state, action)
                if success and (next_state not in explored or node.cost + self.game_env.ACTION_COST[action] < explored[next_state]):
                    new_cost = node.cost + self.game_env.ACTION_COST[action]
                    heapq.heappush(heap, Node(next_state, new_cost, action, node))

        return []


    def reconstruct_path(self, goal_node):
        """
        Reconstruct the path from the goal state to the start state.
        :param goal_node: the goal node
        :return: path (list of actions)
        """
        path = []
        current_node = goal_node
        while current_node.parent is not None:
            path.insert(0, current_node.action)
            current_node = current_node.parent
        return path


    # === A* Search ====================================================================================================
    def preprocess_heuristic(self):
        """
        Perform pre-processing (e.g. pre-computing repeatedly used values) necessary for your heuristic,
        """

        #
        #
        # TODO: (Optional) Implement code for any preprocessing required by your heuristic here (if your heuristic
        #  requires preprocessing).
        #
        # If you choose to implement code here, you should call this method from your search_a_star method (e.g. once at
        # the beginning of your search).
        #
        #
        self.gem_to_exit_distances = []
        exit_pos = (self.game_env.exit_row, self.game_env.exit_col)

        for gem_pos in self.game_env.gem_positions:
            distance = self.euclidean_distance(gem_pos, exit_pos)
            self.gem_to_exit_distances.append(distance)

        

    def compute_heuristic(self, state):
        """
        Compute a heuristic value h(n) for the given state.
        :param state: given state (GameState object)
        :return a real number h(n)
        """

        #
        #
        # TODO: Implement your heuristic function for A* search here. Note that your heuristic can be tested on
        #  gradescope even if you have not yet implemented search_a_star.
        #
        # You should call this method from your search_a_star method (e.g. every time you need to compute a heuristic
        # value for a state)..

        # Calculate Euclidean distance to the exit square
        player_pos = (state.row, state.col)
        exit_pos = (self.game_env.exit_row, self.game_env.exit_col)

        heuristic_value = self.euclidean_distance(player_pos, exit_pos)

        # If there are gems remaining, calculate Euclidean distances to the gems
        if any(gem_status == 0 for gem_status in state.gem_status):
            for gem_idx, gem_status in enumerate(state.gem_status):
                if gem_status == 0:
                    gem_pos = self.game_env.gem_positions[gem_idx]
                    heuristic_value += self.euclidean_distance(player_pos, gem_pos)

        # Scale down the heuristic value for more accurate estimation
        heuristic_value /= 1.2  # Considering the cost of gliding actions

        return heuristic_value

    
    def euclidean_distance(self, pos1, pos2):
        """
        Calculate the Euclidean distance between two positions.
        :param pos1: tuple (row, col)
        :param pos2: tuple (row, col)
        :return: Euclidean distance
        """
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def search_a_star(self):
        """
        Find a path which solves the environment using A* Search.
        :return: path (list of actions, where each action is an element of GameEnv.ACTIONS)
        """

        #
        #
        # TODO: Implement your A*Search algorithm here.
        #
        #
        # Preprocess any required data for the heuristic
        self.preprocess_heuristic()

        start_state = self.game_env.get_init_state()
        start_node = Node(start_state, heuristic=self.compute_heuristic(start_state))
        heap = [start_node]
        open_set = {start_state}  # Use a set to keep track of states in the open set
        closed_set = set()  # Use a set to keep track of explored states
        nodes_expanded = 0

        while heap:
            nodes_expanded += 1
            print("Nodes expanded:", nodes_expanded)
            nodes_on_fringe = len(heap)  # Get the number of nodes on the fringe when the search terminates
            print("Nodes on fringe:", nodes_on_fringe)
            node = heapq.heappop(heap)
            current_state = node.state

            open_set.remove(current_state)  # Remove the state from open set
            closed_set.add(current_state)   # Add the state to closed set

            if self.game_env.is_solved(current_state):
                return self.reconstruct_path(node)

            for action in self.game_env.ACTIONS:
                success, next_state = self.game_env.perform_action(current_state, action)
                if success and next_state not in closed_set:
                    new_cost = node.cost + self.game_env.ACTION_COST[action]
                    heuristic_value = self.compute_heuristic(next_state)

                    if next_state not in open_set:  # Only add to open set if not already there
                        heapq.heappush(heap, Node(next_state, new_cost, action, node, heuristic=heuristic_value))
                        open_set.add(next_state)

        return []