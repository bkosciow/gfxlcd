# -*- coding: utf-8 -*-

"""setup for GfxLCD package"""

import os
from setuptools import setup, find_packages


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as file_handler:
        return file_handler.read()

setup(
    name='gfxlcd',
    version='0.2.0',
    description='gfxlcd is a handler for grpahical lcds: ILI9328, SSD1306, NJU6450 @ Raspberry Pi.',
    keywords=['gfxlcd', 'raspberry pi' ,'ili9328' ,'ssd1306', 'nju6450', 'lcd', 'graphical lcd'],
    long_description=(read('readme.md')),
    url='https://github.com/bkosciow/gfxlcd',
    license='MIT',
    author='Bartosz Kościów',
    author_email='kosci1@gmail.com',
    py_modules=['gfxlcd'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Home Automation'
    ],
    packages=find_packages(exclude=['tests*']),
)
