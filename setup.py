from setuptools import setup, find_packages

setup(
    name="chaturbate-api",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["aiohttp", "aiolimiter", "python-dotenv"],
    entry_points={"console_scripts": ["chaturbate-poller = chaturbate_api.main:main"]},
    author="MountainGod2",
    author_email="admin@reid.ca",
    description="Chaturbate API integration",
    url="https://github.com/MountainGod2/chaturbate-api",
    license="MIT",
)
