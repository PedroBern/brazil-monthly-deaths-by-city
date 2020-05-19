#!/usr/bin/env python

import io
import os
import re
from collections import OrderedDict

from setuptools import find_packages, setup


def get_version(package):
    with io.open(os.path.join(package, "__init__.py")) as f:
        pattern = r'^__version__ = [\'"]([^\'"]*)[\'"]'
        return re.search(pattern, f.read(), re.MULTILINE).group(1)


tests_require = [
    "pytest>=5.4.2",
    "pytest-cov>=2.8.1",
    "coveralls>=2.0.0",
]

dev_requires = ["black==19.10b0", "flake8==3.8.1"] + tests_require

setup(
    name="brazil_monthly_deaths",
    version=get_version("brazil_monthly_deaths"),
    license="MIT",
    description="Brazil deaths by city as pandas dataframe or csv file",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    author="pedrobern",
    author_email="pedrobermoreira@gmail.com",
    maintainer="pedrobern",
    url="https://github.com/pedrobern/brazil-monthly-deaths-by-city",
    project_urls=OrderedDict(
        (
            (
                "Documentation",
                "https://github.com/pedrobern/brazil-monthly-deaths-by-city",
            ),
            (
                "Issues",
                "https://github.com/pedrobern/brazil-monthly-deaths-by-city/issues",
            ),
        )
    ),
    packages=find_packages(exclude=["tests*"]),
    install_requires=["pandas>=1.0.0", "numpy>=1.18.0", "selenium>=3.141.0"],
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="brazil death rate data science",
    zip_safe=False,
    include_package_data=True,
    extras_require={"test": tests_require, "dev": dev_requires},
)
