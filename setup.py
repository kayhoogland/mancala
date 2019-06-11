import setuptools
from setuptools import setup

PACKAGE_NAME = "mancala"
setup(
    name=PACKAGE_NAME,
    python_requires='>=3.6',
    version="0.1.0",
    url="<git url>",
    author="Kay Hoogland",
    author_email="hello@kayhoogland.nl",
    description="Mancala game setup and solver",
    # long_description=open('README.md').read().decode('utf-8'),
    packages=setuptools.find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        "numpy==1.16.3",
        "pandas>=0.24.2",
        "tqdm>=4.32.1"
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': ['mancala=mancala.api.cli:cli']
    },
    package_data={},
    include_package_data=True,
    zip_safe=True,
)
