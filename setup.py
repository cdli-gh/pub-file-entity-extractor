from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name = "Publication File Processor",
    version = "1.0",
    packages = find_packages(),
    install_requires = requirements
)