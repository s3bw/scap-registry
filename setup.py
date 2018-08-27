from setuptools import setup
from setuptools import find_packages


setup(
    name='scap-registry',
    version='0.0.1',
    packages=find_packages(
        include=[
            'scap_lib',
            'scap_registry',
        ]
    ),
    install_requires=[
        'flask==1.0.2',
        'requests==2.19.1',
        'PyYAML==3.13',
    ]
)
