from setuptools import setup


setup(
    name='mezzanine-slides',
    version='2.0.1',
    license='Simplified BSD',

    install_requires=[
        'Mezzanine >= 3.1.7',
        'six >= 1.5.2'],

    description='Easily plug a slideshow into your mezzanine website on all pages.',
    long_description=open('README.rst').read(),

    author='Isaac Bythewood',
    author_email='isaac@bythewood.me',

    url='http://github.com/overshard/mezzanine-slides',
    download_url='http://github.com/overshard/mezzanine-slides/downloads',

    include_package_data=True,

    packages=['mezzanine_slides'],

    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django'])
