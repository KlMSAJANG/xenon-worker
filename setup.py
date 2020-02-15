from setuptools import setup, find_packages

setup(
    name='discord_worker',
    version='0.0.1',
    description='Small Library for building a discord bot on top of rabbitmq',
    url='git@github.com:Magic-Bots/discord-worker',
    author='Merlintor',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.6',
)