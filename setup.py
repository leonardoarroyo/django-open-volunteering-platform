# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='ovp-faq',
    version='0.1.0',
    author=u'Atados',
    author_email='fabio@atados.com.br',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/OpenVolunteeringPlatform/ovp-faq',
    download_url = 'https://github.com/OpenVolunteeringPlatform/ovp-faq/tarball/0.1.0',
    license='AGPL',
    description='This module implements core FAQ functionality.',
    long_description=open('README.rst', encoding='utf-8').read(),
    zip_safe=False,
    install_requires = [
      'Django>=1.10.1,<1.11.0',
      'djangorestframework>=3.5.0,<3.6.0',
      'djangorestframework-jwt>=1.8.0,<2.0.0',
    ]
)
