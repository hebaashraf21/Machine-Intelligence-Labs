# This file contains the options that you should modify to solve Question 2

def question2_1():
    # Setting a slightly higher noise encourages exploration
 
    return {
        "noise": 0.2,
        "discount_factor": 1,     # Discount factor less than 1 for a short-term focus
        "living_reward": -3   # A larger negative living reward promotes aversion to long paths
    }

def question2_2():
    # Opting for a safer path over a dangerous one
    # Choosing the first small exit reward over the second large exit reward

    return {
        "noise": 0.2,
        "discount_factor": 0.3,     # A moderate discount factor of 0.3 for balanced short and long-term considerations
        "living_reward": -1  # A small negative living reward to avoid overly long paths
    }

def question2_3():
    # Preferring the dangerous path over the safe one
    # Opting for the second large exit reward over the first small exit reward
    
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -2 # A higher negative living reward, yet less than question2_1, to encourage the second large exit
    }

def question2_4():
    # Preferring the safe path over the dangerous one
    # Choosing the second large exit reward over the first small exit reward
    
    return {
        "noise": 0.2,
        "discount_factor": 1.0,
        "living_reward": -0.2 # A small negative living reward to discourage overly long paths
    }

def question2_5():
    # Designing the policy to avoid any terminal state and keep the episode going on forever
    
    return {
        "noise": 0.0, # No noise (deterministic environment) to ensure a consistent policy
        "discount_factor": 1,  # A discount factor of 1.0 for a focus on short-term rewards
        "living_reward": 10  # A positive living reward to encourage perpetual exploration
    }

def question2_6():
    # Designing the policy to seek the exit as fast as possible

    return {
        "noise": 0,       # No noise (deterministic environment) to ensure a direct path
        "discount_factor": 1.0,     # A discount factor of 1.0 for a focus on short-term rewards
        "living_reward": -25     # A large negative living reward to incentivize reaching the exit quickly
    }
