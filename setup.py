from setuptools import setup
from setuptools import find_packages


setup(
    packages=find_packages(
        include=[
            'scap_lib',
            'scap_registry',
        ]
    )
)
