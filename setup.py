from setuptools import setup, find_packages

setup(
    name='xiaoaitts',
    packages=find_packages(where='.'),
    version='0.0.0',
    description='the TTS API for XiaoAi Wifispeaker.',
    keywords='xiaoai wifispeaker TTS API',
    author='barriery',
    url='https://github.com/barrierye/xiaoaitts',
    install_requires=[
        'requests==2.31.0',
    ],
)
