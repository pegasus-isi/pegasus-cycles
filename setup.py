# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup

install_requires = ["Click", "netCDF4"]


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def find_package_data(dirname):
    def find_paths(dirname):
        items = []
        for fname in os.listdir(dirname):
            path = os.path.join(dirname, fname)
            if os.path.isdir(path):
                items += find_paths(path)
            elif not path.endswith(".py") and not path.endswith(".pyc"):
                items.append(path)
        return items

    items = find_paths(dirname)
    return [os.path.relpath(path, dirname) for path in items]


setup(
    name="pegasus_cycles",
    version="0.0.0",
    author="Rajiv Mayani",
    author_email="mayani@isi.edu",
    description="Pegasus Cycles",
    long_description=read("README.md"),
    license="Apache",
    url="https://pegasus.isi.edu",
    classifiers=[
        "Topic :: Internet :: WWW/HTTP :: Application",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
    ],
    entry_points={"console_scripts": ["pegasus-cycles = pegasus_cycles.__main__:cli"]},
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["pegasus_cycles.tests*"]),
    package_data={"pegasus_cycles": find_package_data("src/pegasus_cycles")},
    exclude_package_data={"pegasus_cycles": ["tests/*"]},
    zip_safe=False,
    install_requires=install_requires,
    test_suite="pegasus_cycles.tests",
)
