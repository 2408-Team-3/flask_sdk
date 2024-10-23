from setuptools import setup, find_packages

setup(
    name='error_monitor',
    version='0.1.1',
    install_requires=[
      'Flask',
      'requests',
      'uuid',
      'datetime',
      'traceback'
    ],
    python_requires='>=3.6'
)