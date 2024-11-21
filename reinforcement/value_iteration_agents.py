# value_iteration_agents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# value_iteration_agents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learning_agents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learning_agents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.get_states()
              mdp.get_possible_actions(state)
              mdp.get_transition_states_and_probs(state, action)
              mdp.get_reward(state, action, next_state)
              mdp.is_terminal(state)
        """
        super().__init__()
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.run_value_iteration()
    
    def run_value_iteration(self):
        """
          Run the value iteration algorithm. Note that in standard
          value iteration, V_k+1(...) depends on V_k(...)'s.
        """
        "*** YOUR CODE HERE ***"
        for _ in range(self.iterations): # Since the number of iterations is limited
            new_values = util.Counter() # We initialize the values of our collection of new values
            for state in self.mdp.get_states():
                if self.mdp.is_terminal(state):
                    new_values[state] = 0  # Terminal states keep the value 0 since you can't keep moving once you make it to them
                else:
                    # Find the maximum Q-value over all actions
                    possible_actions = self.mdp.get_possible_actions(state)
                    new_values[state] = max(
                        self.compute_q_value_from_values(state, action)
                        for action in possible_actions
                    )
            self.values = new_values  # Update values after processing all states
            
    def get_value(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def compute_q_value_from_values(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # We apply the formula seen in theory: Q(s,a)= ∑P(s′∣s,a)[R(s,a,s′)+γV(s′)]
        q_value = 0 # q_value = Q(s,a)
        for next_state, prob in self.mdp.get_transition_states_and_probs(state, action): # Represents the sum '∑' part
            reward = self.mdp.get_reward(state, action, next_state) # reward = R(s,a,s′)
            q_value += prob * (reward + self.discount * self.values[next_state]) # P(s′∣s,a) * ( reward + γ * V(s′)])
        return q_value

    def compute_action_from_values(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.is_terminal(state):
            return None  # No actions available in terminal states
        
        possible_actions = self.mdp.get_possible_actions(state)
        best_action = None
        best_q_value = float('-inf')

        for action in possible_actions: # We iterate all action an set as best_action the one with higher q_value 
            q_value = self.compute_q_value_from_values(state, action)
            if q_value > best_q_value:
                best_q_value = q_value
                best_action = action

        return best_action

    def get_policy(self, state):
        return self.compute_action_from_values(state)

    def get_action(self, state):
        """Returns the policy at the state (no exploration)."""
        return self.compute_action_from_values(state)

    def get_q_value(self, state, action):
        return self.compute_q_value_from_values(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learning_agents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.get_states()
              mdp.get_possible_actions(state)
              mdp.get_transition_states_and_probs(state, action)
              mdp.get_reward(state)
              mdp.is_terminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def run_value_iteration(self):
        """*** YOUR CODE HERE ***"""

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learning_agents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def run_value_iteration(self):
        """*** YOUR CODE HERE ***"""

