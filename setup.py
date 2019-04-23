import setuptools


setuptools.setup(
    name="stocktrends",
    version="0.1.4",
    url="https://github.com/chillaranand/stocktrends",

    author="chillar anand",
    author_email="chillar@avilpage.com",

    description="Python package to plot stock trends with charts like renko, line break, pnf etc",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
