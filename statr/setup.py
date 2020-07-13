from setuptools import setup

setup(
    name='statr',
    version='0.1',
    py_modules=['statr'],
    install_requires=[
        'Click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        statr=main:cli
    ''',
)