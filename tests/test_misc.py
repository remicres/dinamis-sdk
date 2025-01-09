#!/usr/bin/env python

import dinamis_sdk
import pkg_resources

version_from_module = dinamis_sdk.__version__
from importlib.metadata import version, PackageNotFoundError

try:
    version_from_pkg = version("dinamis_sdk")
except PackageNotFoundError:
    # package is not installed
    version_from_pkg = ""

assert version_from_module
assert version_from_pkg
assert version_from_module == version_from_pkg, f"version from module is {version_from_module} but version from pkg is {version_from_pkg}"
