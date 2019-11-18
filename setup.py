from setuptools import setup, find_packages

setup(
    name = 'xiaoaitts',
    packages = find_packages(where='.'),
    version = '0.0.0',
    description = 'xiaoai TTS API',
    author='barriery',
    url='https://github.com/barrierye/xiaoaitts',
    install_requires=[
        'requests==2.22.0',
    ],
)
