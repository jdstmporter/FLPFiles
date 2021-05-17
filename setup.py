from setuptools import setup, find_packages
from os import path


    
here = path.abspath(path.curdir)
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
scripts=[path.join(here,f'src/parse_flp') ]

packages=find_packages('src')
print(f'Packages is "{packages}"')

setup(
    name='FLPFile',
    version='0.2.0',
    description=f'A simple FL Studio Project File parser',
    long_description=long_description,
    author='Julian Porter',
    author_email='julian@porternet.org',
    url='https://github.com/jdstmporter/FLPFiles.git',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
         'Programming Language :: Python :: 3.9'
    ],
    keywords=['FL Studio Project File','FLP file'],
    packages=packages,
    python_requires='>=3.6, <4',
    package_dir={
        '':'src'
    },
    package_data={
        'data': [f'*.flp']
    },
    data_files=[('/usr/local/bin',scripts)]
)


