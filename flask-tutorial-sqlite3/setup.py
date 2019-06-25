
# The setup.py file describes your project and the files that belong to it
from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    # packages tells Python what package directories (and the Python files they contain) to include
    packages=find_packages(),
    # include static and templates directories referenced in the MANIFEST.in file
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
