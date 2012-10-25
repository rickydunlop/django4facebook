from setuptools import setup, find_packages

setup(
    name='django4facebook',
    version='0.1.1',
    description='Facebook integration for your Django website.',
    long_description=open('README.md').read(),
    author='Aidan Lister',
    author_email='aidan@php.net',
    maintainer='Venelin Stoykov',
    maintainer_email='vstoykov@gmail.com',
    url='https://github.com/vstoykov/django4facebook',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django>=1.2.7',
        'facebook-sdk>0.2.0,>=0.3.1',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
