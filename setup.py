from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='fast_lineage_caller',
version='0.3.1',
description='Module to call Mycobacterium tuberculosis lineages',
url='https://github.com/farhat-lab/fast-lineage-caller/',
author='Luca Freschi',
author_email='l.freschi@gmail.com',
license='LGPLv3',
packages=['fast_lineage_caller',"snp_schemes"],
classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
      ],
      keywords='Mycobacterium tuberculosis lineage calling',
      install_requires=[],
      scripts=['bin/fast-lineage-caller'],
zip_safe=False,
include_package_data=True)
