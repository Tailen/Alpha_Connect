# Calculate reward based on how many steps into the game resulted in a win
# For Connect 4, shortest win is 7 steps and longest win is 42 steps
# 1.18 – (9*step_n/350) results reward to be between interval [0.1, 1]
# the network to prefer faster win and slower loss
# Under the same amount of training, no normalization result in better win ratio
def normalizeReward(step_n, reward):
    return reward*(1.18-(9*step_n/350))