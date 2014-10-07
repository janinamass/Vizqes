import os
import glob
from setuptools import setup, find_packages
setup(
        name='seqPlot',
        version='0.1.0',
        author='Janina Mass',
        author_email='janina.mass@hhu.de',
        packages=['seqplot'],
        scripts=['seqPlot.py'],
        package_data = {'seqplot': ['data/FreeMono.ttf']},	
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
