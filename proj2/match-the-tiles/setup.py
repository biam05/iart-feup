from setuptools import setup, find_packages

setup(
    name="match_the_tiles",
    version="0.0.1",
    description="OpenAI Gym environment for Match the Tiles puzzle",
    install_requires=["gym", "numpy"],
    packages=find_packages()
)