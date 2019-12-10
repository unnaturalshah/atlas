"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import argparse
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path, environ, listdir
from shutil import rmtree

if 'build' in listdir():
    rmtree('build')
if 'dist' in listdir():
    rmtree('dist')
if 'foundations_contrib.egg-info' in listdir('src'):
    rmtree('src/foundations_contrib.egg-info')

cli = environ.get('FOUNDATIONS_CLI', '')
exclude = []

if cli == 'atlas':
    exclude.append('*sub_parsers.monitor*')
    exclude.append('*sub_parsers.orbit*')
    exclude.append('*sub_parsers.setup*')
elif cli == 'orbit':
    exclude.append('*sub_parsers.orbit*')
    exclude.append('*sub_parsers.atlas*')
    exclude.append('*sub_parsers.setup*')

here = path.abspath(path.dirname(__file__))
build_version = environ.get('build_version', '0.0.0')

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def list_files_recursively(root, start_directory):
    import os
    import os.path
    previous_directory = os.getcwd()
    os.chdir(root)
    for directory, _, files in os.walk(start_directory):
        for file in files:
            yield os.path.join(directory, file)
    os.chdir(previous_directory)

package_data = list(list_files_recursively('src/foundations_contrib', 'resources')) + ['resources/*', "**/*pytransform*", "**/license.lic", "*pytransform*", "license.lic", "pytransform.py", "*", "**/*", 'licenses/*/*', 'licenses/*']

package_source = "src"
if environ.get("BUILD_FOUNDATIONS_OBFUSCATED", False):
    package_source = "obfuscated_dist"

setup(
    name='foundations-contrib',
    version=build_version,
    description='A tool for machine learning development - files for contribution',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'tabulate==0.8.3',
        'slackclient==1.3.0',
        'psutil==5.6.2',
        'jsonschema==3.0.2',
        'pyarmor==5.5.6',
        'foundations-internal=={}'.format(build_version),
        'foundations-events=={}'.format(build_version)
    ],
    packages=find_packages(package_source, exclude=exclude),
    package_dir={'': package_source},
    package_data={
        'foundations_contrib': package_data,
    },
)