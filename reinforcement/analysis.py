# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    # The reward of reaching the goal state (+10) is so little compared to
    # the reward of negative terminal states (-100). Therefore, the risk of ending
    # up in a negative state must be very low for crossing the bridge to be 
    # worth it. This is obtained by lowering the noise value and ensuring that the agent
    # always takes the desired action (left or right).
    answer_discount = 0.9
    answer_noise = 0.01 # We make actions more predictable while rewarding long term solutions (answer_discount left as it was)
    return answer_discount, answer_noise

# answer_discount (γ): Represents how much the agent values future rewards compared to immediate rewards.
# answer_noise: Represents the probability that the agent’s action results in an unintended outcome. (if risk is up then it takes safer paths)
# answer_living_reward: Value that the agent gets regardless where it is.

def question3a():
    answer_discount = 0.5  # Focus on mid/short-term rewards (+1)
    answer_noise = 0 # No fear to the risk since it doesn't contemplate an unexpected move
    answer_living_reward = -1 # Big penalty on living so it prefers the first positive terminal state
    return answer_discount, answer_noise, answer_living_reward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    answer_discount = 0.5 # Focus on mid/short-term rewards (+1)
    answer_noise = 0.2 # Avoids the risk
    answer_living_reward = -1 # Big penalty on living so it prefers the first positive terminal state
    return answer_discount, answer_noise, answer_living_reward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    answer_discount = 0.9 # Focus on long-term rewards
    answer_noise = 0 # No fear to the risk since it doesn't contemplate an unexpected move
    answer_living_reward = 0 # No hurry for finishing earlier so it look for the higher terminal state
    return answer_discount, answer_noise, answer_living_reward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    answer_discount = 0.9  # Long-term rewards
    answer_noise = 0.2    # Some uncertainty so it avoids the cliff
    answer_living_reward = -0.1  # Slight penalty for each step
    return answer_discount, answer_noise, answer_living_reward

    # If not possible, return 'NOT POSSIBLE'

def question3e():
    answer_discount = 0.1  # Avoid focusing on future rewards
    answer_noise = 0       # Complete control
    answer_living_reward = 1  # Strong incentive to keep moving
    return answer_discount, answer_noise, answer_living_reward
    # If not possible, return 'NOT POSSIBLE'

def question6():
    """
    Should return EITHER a 2-item tuple of (epsilon, learning rate)
    OR the string 'NOT POSSIBLE' if there is none.
    Epsilon is controlled by -e, learning rate by -l.
    """
    return 'NOT POSSIBLE'

def question8():
    answer_epsilon = None
    answer_learning_rate = None
    return answer_epsilon, answer_learning_rate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
