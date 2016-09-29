from setuptools import setup
setup(
    name = "pyTorify",
    version = "1.0",
    py_modules = ['torify'],
    test_suite = 'test_torify',

    install_requires = ['PySocks>=1.5.6'],

    author = "Willem Hengeveld",
    author_email = "itsme@xs4all.nl",
    description = "Torify python scripts",
    license = "MIT",
    keywords = "TOR networking",
    url = "https://github.com/nlitsme/pytorify/",
    long_description = "Tool for redirecting all TCP traffic over TOR",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        
        'Topic :: Internet :: Proxy Servers',
    ],

)
