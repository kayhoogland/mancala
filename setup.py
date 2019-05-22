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
        "python-telegram-bot>=11.1.0",
        "requests>=2.22.0"
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
    ],
    package_data={},
    include_package_data=True,
    zip_safe=True,
)
