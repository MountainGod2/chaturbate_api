# setup.py

from setuptools import setup, find_packages

setup(
    name="chaturbate_api",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "aiolimiter",
    ],
)
