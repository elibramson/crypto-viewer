from setuptools import setup, find_packages

setup(
    name="crypto-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.100.1",
        "uvicorn==0.15.0",
        "pydantic-settings==2.9.1",
        "python-dotenv==1.1.0",
        "aiohttp==3.12.6",
        "async-lru==2.0.5",
    ],
    extras_require={
        "test": [
            "pytest==7.4.3",
            "pytest-asyncio==0.21.1",
            "pytest-cov==4.1.0",
        ],
    },
) 