import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

meta = dict()  # type: dict
with open(os.path.join(here, "pydrag", "version.py"), encoding="utf-8") as f:
    exec(f.read(), meta)

if __name__ == "__main__":
    setup(
        packages=find_packages(),
        version=meta["version"],
        install_requires=[
            "attrs == 18.2.0",
            "requests == 2.21.0",
            "python-dotenv == 0.10.0",
        ],
        extras_require={
            "dev": [
                "pre-commit",
                "pytest",
                "pytest-cov",
                "codecov",
                "vcrpy",
                "tox",
            ],
            "docs": ["sphinx", "sphinx-rtd-theme", "sphinx-autodoc-typehints"],
        },
    )
