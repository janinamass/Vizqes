import os
import glob
from setuptools import setup, find_packages
setup(
        name='seqPlot',
        version='0.0.1',
        author='Janina Mass',
        author_email='janina.mass@hhu.de',
        packages=['seqplot'],
        scripts=['seqplot/seqPlot.py'],
	license='GPLv3',
        url='https://pypi.python.org/pypi/seqSieve/',
        description='Remove outlier sequences from multiple sequence alignment',
        long_description=open('README.md').read(),
       	include_package_data=True, 
	classifiers=[
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Bio-Informatics'
            ],
        )
