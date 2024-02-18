from setuptools import setup, find_packages

setup(
    name="cbapi",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["aiohttp", "aiolimiter", "python-dotenv"],
    entry_points={"console_scripts": ["cbapi = cbapi.api_client:main"]},
    author="MountainGod2",
    author_email="admin@reid.ca",
    description="Package for interacting with the Chaturbate API",
    url="https://github.com/MountainGod2/cbapi",
)
