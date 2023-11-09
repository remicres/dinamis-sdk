from setuptools import setup, find_packages

install_requires = [
    "requests",
    "qrcode",
    "appdirs",
    "pydantic",
    "pystac",
    "pystac_client",
    "pydantic>=1.7.3",
    "packaging"
]

setup(
    name="dinamis-sdk",
    version="0.0.14",
    description="DINAMIS SDK",
    python_requires=">=3.8",
    author="Remi Cresson",
    author_email="remi.cresson@inrae.fr",
    license="MIT",
    zip_safe=False,
    install_requires=install_requires,
    packages=find_packages(),
)

