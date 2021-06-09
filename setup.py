import setuptools


setuptools.setup(
    name="stocktrends",
    version="0.1.5",
    url="https://github.com/chillaranand/stocktrends",

    author="chillar anand",
    author_email="chillar@avilpage.com",

    description="Python package to plot stock, derivative(futures & options) trends with charts like renko, line break, pnf etc",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
