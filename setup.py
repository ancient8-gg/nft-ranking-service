"""Setup script for Rarity Service."""

from setuptools import setup, find_packages

setup(
    name="rarity-service",
    version="1.0.0",
    description="A service for calculating NFT rarity rankings",
    author="Space3",
    author_email="info@space3.xyz",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # IMPORTANT: Python 3.10 or 3.11 only. Python 3.12+ is not compatible with OpenRarity
    python_requires=">=3.10, <3.12",
    install_requires=[
        "pymongo>=4.6.0",
        "python-dotenv>=1.0.0",
        "schedule>=1.2.0",
        "open-rarity>=0.7.5",
    ],
    entry_points={
        "console_scripts": [
            "rarity-service=rarity_service.cli:main",
        ],
    },
) 