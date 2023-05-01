from setuptools import setup
from setuptools import find_packages


VERSION = '0.0.1'

setup(
    name='matcolor',  # package name
    version=VERSION,  # package version
    author="Casea",
    description='Provide more color schemes for matplotlib',  # package description
    packages=["matcolor"],
    include_package_data=True,
    package_data={
        'colorschemes': ['dcolor.yaml'],
    },
    exclude_package_data={"test":["*"]},
    install_requires=[
        "matplotlib>=3.5",
        "numpy",
        "PyYAML",
        "pillow",
    ],
)