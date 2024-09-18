from setuptools import setup, find_packages

install_requires = [
    "requests",
    "qrcode",
    "appdirs",
    "pystac",
    "pystac_client",
    "pydantic>=1.7.3",
    "pydantic_settings",
    "packaging"
]

setup(
    name="dinamis-sdk",
    version="0.2.1",
    description="DINAMIS SDK",
    python_requires=">=3.8",
    author="Remi Cresson",
    author_email="remi.cresson@inrae.fr",
    license="MIT",
    zip_safe=False,
    install_requires=install_requires,
    packages=find_packages(),
)

