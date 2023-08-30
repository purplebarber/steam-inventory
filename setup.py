from setuptools import setup

setup(
    name='steam-inventory',
    version='1.0.0',
    packages=[
        'steam_inventory'
    ],
    install_requires=[
        'httpx'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='steam inventory, steam, steam inventory api, steam inventory api bypass, steam inventory bypass',
    url='https://github.com/purplebarber/steam-inventory',
    license='MIT',
    author='Purple Barber',
    author_email='',
    description='A simple python package that uses proxies to bypass steam\'s rate limits on their game inventory API.'
)
