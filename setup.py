#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="rtsm",
    version="0.1.0",
    description="Real-Time System Monitor - A Neofetch-like tool with continuous updates",
    author="RTSM Team",
    author_email="example@example.com",
    url="https://github.com/example/rtsm",
    packages=find_packages(),
    install_requires=[
        "psutil>=5.9.0",
    ],
    extras_require={
        "gpu": ["GPUtil>=1.4.0"],
    },
    entry_points={
        "console_scripts": [
            "rtsm=rtsm.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console :: Curses",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.6",
)