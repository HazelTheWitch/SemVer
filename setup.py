from setuptools import setup, find_packages
from pathlib import Path

from src.semver import version


here = Path(__file__).parent.resolve()

long = (here / 'README.md').read_text('utf-8')
short = long.split('\n')[1]

setup(
    name='semver',
    version=version.string,
    description=short,
    long_description=long,
    long_description_content_type='text/markdown',
    url='https://github.com/HazelTheWitch/SemVer',
    author='Hazel Rella',
    author_email='hazelrella11@gmail.com',
    classifiers=[
        'Development Status :: 5 - Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='versioning, version, semantic version',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.7, <4'
)
