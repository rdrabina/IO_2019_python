from setuptools import setup
from setuptools import find_packages

long_description = '''
agar is remake of well known game: agar.io
'''

setup(name='agar',
      version='0.1.0',
      description='server for agar',
      long_description=long_description,
      author='IOfighters',
      author_email='IO@fighters.io',
      url='https://github.com/rdrabina/IO_2019_python',
      download_url='',
      license='MIT',
      install_requires=['numpy>=1.16.3',
                        'collision>=1.2.2'],
      extras_require={
          'tests': ['pytest',
                    'markdown'],
      },
      classifiers=[
          'Development Status :: 1 - Development',
          'Intended Audience :: Gamers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Topic :: Games :: Game',
      ],
      packages=find_packages())
