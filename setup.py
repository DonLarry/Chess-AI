from setuptools import setup


setup(
    name='chess_engine',
    version='0.0.1',
    description='',
    url='https://github.com/DonLarry/Chess-AI',
    license='MIT License',
    packages=['src'],
    install_requires=[
        'chess',
        'pyswip',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)
