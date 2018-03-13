from setuptools import setup

setup(
    name='evesh',
    version='0.1',
    py_modules=['evesh'],
    install_requires=[
        'Click',
        'Requests'
    ],
    entry_points='''
        [console_scripts]   
        evesh=evesh:cli
    '''
)       
