import gym
import gym_pigchase_topdown

env = gym.make('PigChase-v0')

_ = env.reset()
env.render()
done = False

while True:
	action = env.read_action()
	if action != -1:
		_, reward, done, _ = env.step(action)
		print(reward)

	env.render()

	if done:
		break