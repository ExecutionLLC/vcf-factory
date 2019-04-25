from setuptools import find_packages
from setuptools import setup

import vcf_factory

setup(
    name='vcf-factory',
    version=vcf_factory.__version__,
    license=vcf_factory.__license__,
    description='Tools for automatic generate pleasible VCF-files',
    author=vcf_factory.__author__,
    author_email='anton.konovalov1976@gmail.com',
    url='https://github.com/ExecutionLLC/vcf-factory',
    py_modules=['vcf_factory', 'vcf_consts'],
    keywords=['vcf', 'factory'],
    python_requires='>=2.6, !=3.0.*, !=3.1.*',
    zip_safe=False,
    platforms='any',
)
