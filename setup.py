# coding: utf8


# --------------------------------------------------------------------------------
# > Imports
# --------------------------------------------------------------------------------
# Built-in
from distutils.core import setup

# Third-party

# Local


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='sudoku_manager',
    packages=['sudoku_manager'],
    version='1.0.5',
    license='MIT',
    description='Package to easily generate and/or solve any 9x9 sudoku grid',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jordan Kowal',
    author_email='kowaljordan@gmail.com',
    url='https://github.com/Jordan-Kowal/sudoku_manager',
    download_url='https://github.com/Jordan-Kowal/sudoku_manager/archive/v1.0.5.tar.gz',
    keywords=['sudoku', 'generator', 'solver', 'easy', "generate", "solve"],
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
