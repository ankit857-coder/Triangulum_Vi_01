"""
Minimal setup.py for compatibility with older tools.
For actual configuration, see pyproject.toml
"""

from setuptools import setup

if __name__ == "__main__":
    setup(
        name="triangulum-vi-01",
        packages=["triangulum"],
    )
