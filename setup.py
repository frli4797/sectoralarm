from distutils.core import setup

setup(
    name='sectoralarm',
    version='1.0.1',
    packages=['sectoralarm'],
    url='https://github.com/MikaelSchultz/sectoralarm',
    license='MIT License',
    author='Mikael Schultz',
    author_email='mikael@dofiloop.com',
    description='A simple library for Sector Alarm API.',
    install_requires=[
          'requests',
    ],
)
