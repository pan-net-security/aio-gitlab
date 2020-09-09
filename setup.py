from setuptools import setup

setup(
    name='aio-gitlab',
    version='0.1.0',
    description='A module that allows for faster fetching of resources from Gitlab API using asyncio',
    author='Dominik Bucko',
    author_email='dominik.bucko@pan-net.eu',
    url='',
    packages=['aio-gitlab'],
    install_requires=['python-gitlab==1.6.0', 'aiohttp==3.6.2'],
    keywords=['gitlab', 'asyncio', 'gitlab-ci', 'devops'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
)

