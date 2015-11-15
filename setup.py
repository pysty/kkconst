from setuptools import setup

version = '1.0.2'

setup(
    name='kkconst',
    version=version,
    description="Define const field and const class, customize it as You Like (Python)",
    long_description="Define const field and const class, customize it as You Like (Python)",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
      ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='kkconst',
    author='ZHONG KAIXIANG',
    author_email='xiang.ace@gmail.com',
    url='http://www.kaka-ace.com',
    license='http://opensource.org/licenses/MIT',
    # packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    packages=['kkconst'],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
