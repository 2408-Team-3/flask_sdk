from setuptools import setup, find_packages

setup(
    name='monitor',
    version='0.1.1',
    py_modules=['sdk'],
    packages=find_packages(),
    install_requires=[
      'Flask',
      'requests',
      'uuid'
    ],
    python_requires='>=3.6'
)