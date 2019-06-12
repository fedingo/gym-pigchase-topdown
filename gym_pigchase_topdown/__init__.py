from gym.envs.registration import register

register(id='PigChase-v0',
    entry_point='gym_pigchase_topdown.envs:PigChaseEnv',
    kwargs = {}
)