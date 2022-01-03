from os.path import abspath, dirname, join, isfile
from os import environ
from setuptools import find_packages, setup
import sys
version_f = ".version"
this_dir = abspath(dirname(__file__))
with open(join(this_dir, "README.md"), encoding="utf-8") as file:
    long_description = file.read()


def get_version():
    if isfile(version_f):
        with open(version_f) as version_file:
            version = version_file.read().strip()
            return version
    elif (
        "build" in sys.argv
        or "egg_info" in sys.argv
        or "sdist" in sys.argv
        or "bdist_wheel" in sys.argv
    ):
        version = environ.get("VERSION", "0.0")  # Avoid PEP 440 warning
        if "-SNAPSHOT" in version:
            version = version.replace("-SNAPSHOT", ".0")
        with open(version_f, "w+") as version_file:
            version_file.write(version)
        return version


setup(
    name="freshenv",
    python_requires=">3.7",
    options={"bdist_wheel": {"universal": "1"}},
    version=get_version(),
    description="A cli to provision and manage local developer environments.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/raiyanyahya/freshenv",
    author="Raiyan Yahya",
    author_email="raiyanyahyadeveloper@gmail.com",
    keywords=["cli","developer-tools","productivity"],
    packages=find_packages(),
    install_requires=["click==8.0.3", "docker==5.0.3", "rich==10.16.2", "dockerpty==0.4.1"],
    entry_points={"console_scripts": ["freshenv=freshenv.cli:cli"]},
)
