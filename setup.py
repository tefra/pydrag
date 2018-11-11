from setuptools import find_packages, setup

classifiers = [
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",
]

install_requires = [
    "attrs == 18.2.0",
    "cattrs == 0.9.0",
    "certifi == 2018.10.15",
    "chardet == 3.0.4",
    "idna == 2.7",
    "python-dotenv == 0.9.1",
    "requests == 2.20.1",
    "urllib3 == 1.24.1",
]

if __name__ == "__main__":
    with open("README.md") as f:
        readme = f.read()

    setup(
        name="pydrag",
        packages=find_packages("pydrag"),
        package_dir={"": "pydrag"},
        install_requires=install_requires,
        author="Christodoulos Tsoulloftas",
        author_email="chris@komposta.net",
        classifiers=classifiers,
        description="A modern Last.fm api wrapper",
        license="MIT",
        url="https://github.com/tefra/pydrag",
        long_description=readme,
    )
