""" Setup for python-senz-wifi-module """

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='senzwifi',
    version='0.0.1',
    description='Python module for working with the senz wifi climate devices ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sockless-coding/python-senz-wifi-module',
    author='sockless-coding',
    license='MIT',
    classifiers=[
       'Topic :: Home Automation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='home automation senz climate',
    install_requires=['requests>=2.20.0'],
    packages=['senzwifi'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'senzwifi=senzwifi.__main__:main',
        ]
    })
