"""Setup file for the chaturbate-api package."""
from setuptools import find_packages, setup

setup(
    name="chaturbate_api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["aiohttp", "aiolimiter", "python-dotenv"],
    entry_points={
        "console_scripts": [
            "chaturbate-api=chaturbate_api.__main__:main",
        ],
    },
    author="MountainGod2",
    author_email="admin@reid.ca",
    description="Chaturbate API integration",
    url="https://github.com/MountainGod2/chaturbate-api",
    license="MIT",
)
