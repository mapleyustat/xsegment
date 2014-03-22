from setuptools import setup, find_packages



kw = dict(
    name='pynettool',
    version='0.0.3',
    description='chinese words segment use regular ',
    author='intoblack',
    author_email='intoblack86@gmail.com',
    url='https://github.com/intoblack/xsegment',
    download_url='https://github.com/intoblack/xsegment',
    platforms='all platform',
    packages=find_packages(),
    include_package_data=True
)

setup(**kw)

