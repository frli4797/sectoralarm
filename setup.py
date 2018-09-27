from distutils.core import setup

setup(
    name='sectoralarm',
    version='1.0.2.3',
    packages=['sectoralarm'],
    url='hhttps://github.com/frli4797/sectoralarm',
    license='MIT License',
    author='Fredrik Jagare',
    author_email='',
    description='A simple library for Sector Alarm API. Heavily relies on Michael Schultz.',
    install_requires=[
          'requests',
    ],
)