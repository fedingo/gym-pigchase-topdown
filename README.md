# gym-pigchase-topdown
PigChase Implementation with a top down view

Grid World implementation of the Pig Chase game from the Marlo Challenge (https://www.crowdai.org/challenges/marlo-2018)

The goal is for the agent to cooperate with the other agent to catch the Pig. The Pig is caught if he does not have any possible moves anymore. 

## Rules

The game has 5 possible actions: Forward, Backward, Turn Left, Right and Stay Still. 

The Reward function has 3 possible values:
- If the pig is stuck, the agents have catched him, so the reward if +1
- If one of the agents reaches the exit, the reward is +0.2 (just for that agent)
- -0.04 otherwise
