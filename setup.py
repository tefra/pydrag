from setuptools import setup

install_requires = ["attrs == 18.2.0", "requests == 2.20.1"]

if __name__ == "__main__":
    setup(
        packages=["pydrag"],
        package_dir={"pydrag": "pydrag"},
        install_requires=install_requires,
    )
