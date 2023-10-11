import sys
import time
import random
import numpy as np
from transition_restricted import *

from game_env import GameEnv
from game_state import GameState
"""
solution.py

This file is a template you should use to implement your solution.

You should implement each of the method stubs below. You may add additional methods and/or classes to this file if you 
wish. You may also create additional source files and import to this file if you wish.

COMP3702 Assignment 2 "Dragon Game" Support Code

Last updated by njc 30/08/23
"""

class StateKey:
    def __init__(self, row, col, gem_status):
        self.row = row
        self.col = col
        self.gem_status = tuple(gem_status)

    def __hash__(self):
        return hash((self.row, self.col, self.gem_status))

    def __eq__(self, other):
        return (self.row, self.col, self.gem_status) == (other.row, other.col, other.gem_status)

class Solver:

    def __init__(self, game_env: GameEnv):
        self.game_env = game_env
        #
        # TODO: Define any class instance variables you require (e.g. dictionary mapping state to VI value) here.
        #
        self.state_values = {}
        self.policy = {}
        self.gamma = game_env.gamma
        self.all_states = self.generate_all_states()
        self.initial_state = game_env.get_init_state()
        self.game_env.ACTIONS = list(self.game_env.ACTIONS)

    def generate_all_states(self):
        """
        Generate a list of all possible game states.
        """
        all_states = []
        n_rows = self.game_env.n_rows
        n_cols = self.game_env.n_cols
        for row in range(n_rows):
            for col in range(n_cols):
                for has_gem in [True, False]:
                    state = GameState(row, col, (1 if has_gem else 0,))
                    all_states.append(state)
        return all_states
    
    def state_to_key(self, state):
        return StateKey(state.row, state.col, state.gem_status)

    def key_to_state(self, key):
        return GameState(key.row, key.col, list(key.gem_status))
    
    @staticmethod
    def testcases_to_attempt():
        """
        Return a list of testcase numbers you want your solution to be evaluated for.
        """
        # TODO: modify below if desired (e.g. disable larger testcases if you're having problems with RAM usage, etc)
        return [1, 2, 3, 4, 5]

    # === Value Iteration ==============================================================================================

    def vi_initialise(self):
        """
        Initialise any variables required before the start of Value Iteration.
        """
        #
        # TODO: Implement any initialisation for Value Iteration (e.g. building a list of states) here. You should not
        #  perform value iteration in this method.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        # Initialize state values (V(s)) for all states to zero.

        for state in self.all_states:
            state_key = StateKey(state.row, state.col, state.gem_status)
            self.state_values[state_key] = 0.0

    def vi_is_converged(self):
        """
        Check if Value Iteration has reached convergence.
        :return: True if converged, False otherwise
        """
        # TODO: Implement code to check if Value Iteration has reached convergence here.
        convergence_threshold = 0.0001
        max_diff = 0.0

        for state in self.all_states:
            state_key = self.state_to_key(state)
            old_value = self.state_values.get(state_key, 0.0)
            new_value = self.calculate_new_value(state)
            diff = abs(new_value - old_value)
            max_diff = max(max_diff, diff)

        return max_diff < convergence_threshold

    
    def calculate_new_value(self, state: GameState):
        """
        Calculate the new value V(s) for a given state based on the Bellman equation.
        :param state: the current state
        :return: the new value V(s)
        """
        if self.is_terminal_state(state):
            return 0.0

        expected_value = 0.0

        for action in self.game_env.ACTIONS:
            action_value = self.calculate_action_value(state, action)
            expected_value = max(expected_value, action_value)

        return expected_value
    
    def calculate_action_value(self, state, action):
        outcomes = []

        if action == self.game_env.WALK_LEFT:
            next_state = GameState(state.row, state.col - 1, state.gem_status)
            if 0 <= next_state.col < self.game_env.n_cols:
                if isinstance(next_state.gem_status, int):
                    next_state.gem_status = (next_state.gem_status,)
                elif not isinstance(next_state.gem_status, tuple) or len(next_state.gem_status) != 1:
                    raise ValueError("gem_status should be an integer or a tuple of length 1")
                outcomes = get_transition_outcomes_restricted(self.game_env, next_state, action)

        if action == self.game_env.WALK_RIGHT:
            next_state = GameState(state.row, state.col + 1, state.gem_status)
            if 0 <= next_state.col < self.game_env.n_cols:
                if isinstance(next_state.gem_status, int):
                    next_state.gem_status = (next_state.gem_status,)
                elif not isinstance(next_state.gem_status, tuple) or len(next_state.gem_status) != 1:
                    raise ValueError("gem_status should be an integer or a tuple of length 1")
                outcomes = get_transition_outcomes_restricted(self.game_env, next_state, action)

        if action == self.game_env.JUMP:
            next_state = GameState(state.row - 1, state.col, state.gem_status)
            if 0 <= next_state.row < self.game_env.n_rows:
                if isinstance(next_state.gem_status, int):
                    next_state.gem_status = (next_state.gem_status,)
                elif not isinstance(next_state.gem_status, tuple) or len(next_state.gem_status) != 1:
                    raise ValueError("gem_status should be an integer or a tuple of length 1")
                outcomes = get_transition_outcomes_restricted(self.game_env, next_state, action)

        action_value = 0.0

        for next_state, reward, transition_prob in outcomes:
            if self.is_terminal_state(next_state):
                action_value += transition_prob * 0
            else:
                if reward is None:
                    # Handle the case where reward is None by setting it to 0.0
                    reward = 0.0
                action_value += transition_prob * (reward + self.gamma * self.vi_get_state_value(next_state))

        return action_value

    def vi_iteration(self):
        """
        Perform a single iteration of Value Iteration (i.e. loop over the state space once).
        """
        #
        # TODO: Implement code to perform a single iteration of Value Iteration here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        # Create a copy of state_values to perform in-place updates
        new_state_values = self.state_values.copy()

        for state in self.all_states:
            if not self.is_terminal_state(state):
                best_action = self.vi_select_action(state)
                if best_action is not None:
                    action_value = self.calculate_action_value(state, best_action)
                    new_state_values[state] = action_value

        self.state_values = new_state_values


    def is_terminal_state(self, state):
        """
        Check if a given state is terminal based on your game's logic.
        :param state: the state to check
        :return: True if the state is terminal, False otherwise
        """
        # Implement the logic to check for terminal states in your game
        # For example, you can check if all gems have been collected and the player has reached a certain position.
        # Replace this with your actual terminal state check.
        # For example, in Dragon Game, you can check if the player has reached the goal and collected all gems.
        all_gems_collected = all(status == 1 for status in state.gem_status)
        at_exit = state.row == self.game_env.exit_row and state.col == self.game_env.exit_col

        return all_gems_collected and at_exit

    def vi_plan_offline(self):
        """
        Plan using Value Iteration.
        """
        # !!! In order to ensure compatibility with tester, you should not modify this method !!!
        self.vi_initialise()
        while True:
            self.vi_iteration()

            # NOTE: vi_iteration is always called before vi_is_converged
            if self.vi_is_converged():
                break

    def vi_get_state_value(self, state: GameState):
        """
        Retrieve V(s) for the given state.
        :param state: the current state
        :return: V(s)
        """
        #
        # TODO: Implement code to return the value V(s) for the given state (based on your stored VI values) here. If a
        #  value for V(s) has not yet been computed, this function should return 0.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        state_key = self.state_to_key(state)
        return self.state_values.get(state_key, 0.0)

    def vi_select_action(self, state: GameState):
        """
        Retrieve the optimal action for the given state (based on values computed by Value Iteration).
        :param state: the current state
        :return: optimal action for the given state (element of ROBOT_ACTIONS)
        """
        #
        # TODO: Implement code to return the optimal action for the given state (based on your stored VI values) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        
        if self.is_terminal_state(state):
            return None

        valid_actions = self.get_possible_actions(state)

        if not valid_actions:
            return None

        return random.choice(valid_actions)
        
    def is_action_valid(self, state, action):
        """
        Check if a given action is valid for the current state.
        :param state: the current state
        :param action: the action to check
        :return: True if the action is valid, False otherwise
        """
        row, col = state.row, state.col
        grid = self.game_env.grid_data

        if action == self.game_env.WALK_LEFT:
            if col > 0:
                next_col = col - 1
                next_tile = grid[row][next_col]
                return next_tile in {GameEnv.AIR_TILE, GameEnv.LADDER_TILE, GameEnv.SUPER_JUMP_TILE, GameEnv.SUPER_CHARGE_TILE}

        elif action == self.game_env.WALK_RIGHT:
            if col < self.game_env.n_cols - 1:
                next_col = col + 1
                next_tile = grid[row][next_col]
                return next_tile in {GameEnv.AIR_TILE, GameEnv.LADDER_TILE, GameEnv.SUPER_JUMP_TILE, GameEnv.SUPER_CHARGE_TILE}

        elif action == self.game_env.JUMP:
            if row > 0:
                next_row = row - 1
                next_tile = grid[next_row][col]
                return next_tile in {GameEnv.AIR_TILE, GameEnv.LADDER_TILE, GameEnv.SUPER_JUMP_TILE, GameEnv.SUPER_CHARGE_TILE}

        elif action == self.game_env.GLIDE_LEFT_1:
            if col > 0 and row < self.game_env.n_rows - 1:
                next_col = col - 1
                next_row = row + 1
                current_tile = grid[row][col]
                next_tile = grid[next_row][next_col]
                return (
                    current_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    next_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE}
                )

        elif action == self.game_env.GLIDE_LEFT_2:
            # Check if gliding left by 2 tiles is valid.
            if col > 1 and row < self.game_env.n_rows - 1:
                next_col = col - 2
                next_row = row + 1
                current_tile = grid[row][col]
                next_tile = grid[next_row][next_col]
                mid_tile = grid[next_row][next_col + 1]
                return (
                    current_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    next_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    mid_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE}
                )

        elif action == self.game_env.GLIDE_LEFT_3:
            # Check if gliding left by 3 tiles is valid.
            if col > 2 and row < self.game_env.n_rows - 1:
                next_col = col - 3
                next_row = row + 1
                current_tile = grid[row][col]
                next_tile = grid[next_row][next_col]
                mid_tile_1 = grid[next_row][next_col + 1]
                mid_tile_2 = grid[next_row][next_col + 2]
                return (
                    current_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    next_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    mid_tile_1 in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    mid_tile_2 in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE}
                )

        elif action == self.game_env.GLIDE_RIGHT_1:
            if col < self.game_env.n_cols - 1 and row < self.game_env.n_rows - 1:
                next_col = col + 1
                next_row = row + 1
                current_tile = grid[row][col]
                next_tile = grid[next_row][next_col]
                return (
                    current_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    next_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE}
                )

        elif action == self.game_env.GLIDE_RIGHT_2:
            # Check if gliding right by 2 tiles is valid.
            if col < self.game_env.n_cols - 2 and row < self.game_env.n_rows - 1:
                next_col = col + 2
                next_row = row + 1
                current_tile = grid[row][col]
                next_tile = grid[next_row][next_col]
                mid_tile = grid[next_row][next_col - 1]
                return (
                    current_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    next_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    mid_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE}
                )

        elif action == self.game_env.GLIDE_RIGHT_3:
            # Check if gliding right by 3 tiles is valid.
            if col < self.game_env.n_cols - 3 and row < self.game_env.n_rows - 1:
                next_col = col + 3
                next_row = row + 1
                current_tile = grid[row][col]
                next_tile = grid[next_row][next_col]
                mid_tile_1 = grid[next_row][next_col - 1]
                mid_tile_2 = grid[next_row][next_col - 2]
                return (
                    current_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    next_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    mid_tile_1 in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    mid_tile_2 in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE}
                )

        elif action == self.game_env.DROP_1:
            if row < self.game_env.n_rows - 1:
                next_row = row + 1
                current_tile = grid[row][col]
                next_tile = grid[next_row][col]
                return current_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and \
                    next_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE}

        elif action == self.game_env.DROP_2:
            # Check if dropping down by 2 tiles is valid.
            if row < self.game_env.n_rows - 2:
                next_row = row + 2
                current_tile = grid[row][col]
                next_tile = grid[next_row][col]
                mid_tile = grid[next_row - 1][col]
                return (
                    current_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    next_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    mid_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE}
                )

        elif action == self.game_env.DROP_3:
            # Check if dropping down by 3 tiles is valid.
            if row < self.game_env.n_rows - 3:
                next_row = row + 3
                current_tile = grid[row][col]
                next_tile = grid[next_row][col]
                mid_tile_1 = grid[next_row - 1][col]
                mid_tile_2 = grid[next_row - 2][col]
                return (
                    current_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    next_tile in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    mid_tile_1 in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE} and
                    mid_tile_2 in {GameEnv.LADDER_TILE, GameEnv.AIR_TILE, GameEnv.LAVA_TILE}
                )

        # Add conditions for other actions if needed.

        return False

    
    def get_possible_actions(self, state):
        possible_actions = []
        row, col = state.row, state.col
        grid = self.game_env.grid_data

        if col > 0 and grid[row][col - 1] in {GameEnv.AIR_TILE, GameEnv.LADDER_TILE, GameEnv.SUPER_JUMP_TILE, GameEnv.SUPER_CHARGE_TILE}:
            possible_actions.append(self.game_env.WALK_LEFT)

        if col < self.game_env.n_cols - 1 and grid[row][col + 1] in {GameEnv.AIR_TILE, GameEnv.LADDER_TILE, GameEnv.SUPER_JUMP_TILE, GameEnv.SUPER_CHARGE_TILE}:
            possible_actions.append(self.game_env.WALK_RIGHT)

        if row > 0 and row < self.game_env.n_rows and grid[row - 1][col] in {GameEnv.AIR_TILE, GameEnv.LADDER_TILE, GameEnv.SUPER_JUMP_TILE, GameEnv.SUPER_CHARGE_TILE}:
            possible_actions.append(self.game_env.JUMP)

        return possible_actions

    # === Policy Iteration =============================================================================================

    def pi_initialise(self):
        """
        Initialise any variables required before the start of Policy Iteration.
        """
        #
        # TODO: Implement any initialisation for Policy Iteration (e.g. building a list of states) here. You should not
        #  perform policy iteration in this method. You should assume an initial policy of always move FORWARDS.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        for state in self.all_states:
            state_key = self.state_to_key(state)
            self.policy[state_key] = random.choice([self.game_env.WALK_LEFT, self.game_env.WALK_RIGHT, self.game_env.JUMP, self.game_env.GLIDE_LEFT_1,self.game_env.GLIDE_LEFT_2,
                                                    self.game_env.GLIDE_LEFT_3,self.game_env.DROP_1,self.game_env.DROP_2,self.game_env.DROP_3,
                                                    self.game_env.GLIDE_RIGHT_1,self.game_env.GLIDE_RIGHT_2,self.game_env.GLIDE_RIGHT_3])

    def pi_is_converged(self):
        """
        Check if Policy Iteration has reached convergence.
        :return: True if converged, False otherwise
        """
        #
        # TODO: Implement code to check if Policy Iteration has reached convergence here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        for state in self.all_states:
            current_action = self.policy.get(state, 0)  # Use 0 as the default action
            new_action = self.pi_select_action(state)
            if current_action != new_action:
                return False
        return True
    
    def pi_iteration(self):
        """
        Perform a single iteration of Policy Iteration (i.e. perform one step of policy evaluation and one step of
        policy improvement).
        """
        #
        # TODO: Implement code to perform a single iteration of Policy Iteration (evaluation + improvement) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        while True:
            self.policy_evaluation()
            policy_stable = True
            for state in self.all_states:
                if not self.is_terminal_state(state):
                    state_key = StateKey(state.row, state.col, state.gem_status)
                    old_action = self.policy[state_key]
                    
                    # Create an array to store action values
                    action_values = np.zeros(len(self.game_env.ACTIONS), dtype=float)
                    
                    for action in self.game_env.ACTIONS:
                        action_value = self.calculate_action_value(state, action)
                        # Convert action to an integer before using it as an index
                        action_index = self.game_env.ACTIONS.index(action)
                        action_values[action_index] = action_value

                    # Find the index of the action with the highest value
                    new_action_index = np.argmax(action_values)
                    new_action = self.game_env.ACTIONS[new_action_index]

                    self.policy[state_key] = new_action  # Assign the new action

                    if old_action != new_action:
                        policy_stable = False

            if policy_stable:
                break

    def policy_evaluation(self):
        while True:
            delta = 0
            for state_key in self.state_values:
                state = self.key_to_state(state_key)
                v = self.state_values[state_key]
                action = self.policy[state]
                action_value = self.calculate_action_value(state, action)
                self.state_values[state] = action_value
                delta = max(delta, abs(v - self.state_values[state]))
            if delta < 0.0001:
                break

    def pi_plan_offline(self):
        """
        Plan using Policy Iteration.
        """
        # !!! In order to ensure compatibility with tester, you should not modify this method !!!
        self.pi_initialise()
        while True:
            self.pi_iteration()

            # NOTE: pi_iteration is always called before pi_is_converged
            if self.pi_is_converged():
                break

    def pi_select_action(self, state: GameState):
        """
        Retrieve the optimal action for the given state (based on values computed by Value Iteration).
        :param state: the current state
        :return: optimal action for the given state (element of ROBOT_ACTIONS)
        """
        #
        # TODO: Implement code to return the optimal action for the given state (based on your stored PI policy) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        if self.is_terminal_state(state):
            return random.choice(self.game_env.ACTIONS)

        state_key = StateKey(state.row, state.col, state.gem_status)
        
        try:
            action = self.policy[state_key]
        except KeyError:
            # If the state is not in the policy, choose a random action
            return random.choice(self.game_env.ACTIONS)

        if not self.is_action_valid(state, action):
            return self.handle_invalid_action(state)

        return action

    def handle_invalid_action(self, state):
        valid_actions = self.get_possible_actions(state)
        if valid_actions:
            return random.choice(valid_actions)
        else:
            return 0