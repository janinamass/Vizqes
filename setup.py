import os
import glob
from setuptools import setup, find_packages
setup(
        name='vizqes',
        version='0.9.0',
        author='Janina Mass',
        author_email='janina.mass@hhu.de',
        packages=['vizqespkg'],
        scripts=['vizqes'],
        package_data = {'vizqespkg': ['data/FreeMono.ttf']},
        license='GPLv3',
        url='https://pypi.python.org/pypi/seqPlot/',
        description='Visualize (multiple) sequence alignment (MSA) with colored boxes',
        long_description=open('README.txt').read(),
       	include_package_data=True,
        install_requires=['Pillow'],
        classifiers=[
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Bio-Informatics'
            ],
        )
