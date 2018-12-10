from setuptools import setup

if __name__ == "__main__":
    setup(
        packages=["pydrag"],
        package_dir={"pydrag": "pydrag"},
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
                "dot",
            ],
            "docs": ["sphinx", "sphinx-rtd-theme", "sphinx-autodoc-typehints"],
        },
    )
