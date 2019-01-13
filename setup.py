from setuptools import setup
from setuptools import find_packages


setup(
    name='scap-registry',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'scap-registry = scap_registry.wsgi:run_server',
        ]
    },
    packages=find_packages(
        include=[
            'scap_lib',
            'scap_registry',
        ]
    ),
    package_data={
        'scap_registry': ['../config.yml']
    },
    install_requires=[
        'flask==1.0.2',
        'requests==2.21.0',
        'PyYAML==4.2b1',
        'boto==2.49.0',
        'boto3==1.9.0',
        'botocore==1.12.0',
    ],
    extra_require={
        'test': [
            'tox',
            'pytest',
            'flake8',
        ]
    }
)
