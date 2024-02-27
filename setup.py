from setuptools import find_packages, setup

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="chaturbate_api",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "aiolimiter",
        "python-dotenv",
        "asynctest",
        "pre-commit",
        "vcrpy",
    ],
    entry_points={
        "console_scripts": [
            "chaturbate-api=chaturbate_api.__main__:main",
        ],
    },
    author="MountainGod2",
    author_email="admin@reid.ca",
    description="Chaturbate API integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MountainGod2/chaturbate_api",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    keywords="chaturbate api asyncio",
)
