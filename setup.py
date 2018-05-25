from distutils.core import setup

setup(
    name='sectoralarm',
    version='1.0.2.2',
    packages=['sectoralarm'],
    url='https://github.com/frli4797/sectoralarm',
    license='MIT License',
    author='Fredrik Jägare Lilja',
    author_email='noreply@dummmy.gha',
    description='A simple library for Sector Alarm API.',
    install_requires=[
          'requests',
    ],
)
