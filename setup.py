from setuptools import setup

setup(name='gym_pigchase_topdown',
      version='0.1',
      url="",
      author="Federico Rossetto",
      license="MIT",
      packages=["gym_pigchase_topdown", "gym_pigchase_topdown.envs"],
      install_requires=['gym', 'numpy', 'pygame', 'random']
)