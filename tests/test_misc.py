#!/usr/bin/env python

import dinamis_sdk
import pkg_resources

version_from_module = dinamis_sdk.__version__
version_from_pkg = pkg_resources.require("dinamis-sdk")[0].version
assert version_from_module
assert version_from_pkg
assert version_from_module == version_from_pkg, f"version from module is {version_from_module} but version from pkg is {version_from_pkg}"
