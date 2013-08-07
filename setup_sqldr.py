'''
Created on 07.08.2013

@author: bova
'''
from setuptools import setup
from sqloader import APP_VERSION

setup(name='sqloader',
    version=APP_VERSION,
    description='Squid access log loader',
    author='Vladimir Povetkin',
    author_email='vladimir@fido.uz',
    packages=['sqloader'],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        sqloader = sqloader:main
        """
)
