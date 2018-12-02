from setuptools import setup

install_requires = [
    "attrs == 18.2.0",
    "certifi == 2018.10.15",
    "chardet == 3.0.4",
    "idna == 2.7",
    "python-dotenv == 0.9.1",
    "requests == 2.20.1",
    "urllib3 == 1.24.1",
]

if __name__ == "__main__":
    setup(
        packages=["pydrag"],
        package_dir={"pydrag": "pydrag"},
        install_requires=install_requires,
    )
