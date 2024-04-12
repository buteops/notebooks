#!/usr/bin/env python3

from pathlib import Path
from setuptools import find_packages, setup
from typing import List


directory = Path(__file__).resolve().parent
with open(directory / 'README.md', encoding = 'utf-8') as readme:
    long_description = readme.read()


HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements


setup(
    name="MLOps Notebooks",
    version="1.0.0",
    description = "you interest to mlops? let's train together 👊",
    author="pandohansamuel19",
    license = 'MIT',
    long_description = long_description,
    long_description_content_type='text/markdown',
    python_requires = '>=3.8',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)
