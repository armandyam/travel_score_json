from setuptools import setup, find_packages

setup(
    name='travel-score',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'geopy>=2.3.0',
        'pandas>=1.5.0',
        'numpy>=1.23.0',  # Required by pandas
    ],
    entry_points={
        'console_scripts': [
            'travel-score=travel_score.travel_score:main',
        ],
    },
    author='Your Name',
    description='A tool for processing geographical data and generating location data in JSON format',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='travel geography coordinates geocoding',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
