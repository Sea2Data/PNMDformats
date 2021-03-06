from setuptools import setup

setup(name='pnmdformats',
      version='1.0',
      description='This package provides functionality for downloading, reading and writing xml-formats defined by NMD in PYTHON.',
      url='https://github.com/Sea2Data/PNMDformats',
      author='Sindre Vatnehol',
      author_email='sindre.vatnehol@hi.no',
      license='GPL3',
      packages=['pnmdformats'],
      package_data={'':['example_data\*.nc']},
      zip_safe=False)

