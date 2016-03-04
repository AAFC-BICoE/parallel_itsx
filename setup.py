try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='parallel-itsx',
    version='0.0.dev1',
    packages=['itsx'],
    url='https://github.com/MikeKnowles/parallel-itsx',
    include_package_data=True,
    license='MIT',
    author='mike knowles',
    author_email='mikewknowles@gmail.com',
    description='Parallel ITSx implementation',
    long_description=open('README.md').read(),
    install_requires=['biopython >= 1.65',
                      'argparse >= 1.4.0'],
    scripts=['bin/parallel_itsx'],
)
