from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.2'
DESCRIPTION = 'Pathing library for FTC robotics.'
LONG_DESCRIPTION = 'A package that allows for the control of a robot on a FTC field, specifically meant to work with two wheel differential swerve.'

# Setting up
setup(
    name="InputDriverFTC",
    version=VERSION,
    author="Tiernan Lindauer",
    author_email="<tiernanxkl@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'FTC', 'autonomous', 'robotics'],
    classifiers=[
        "Development Status :: 2 - Release",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)