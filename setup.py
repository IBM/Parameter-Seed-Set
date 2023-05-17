from setuptools import setup, find_packages

setup(name='parameter_seed_set',
      version='0.1',
      packages=find_packages(where="./src/", exclude=['unittests']),
      include_package_data=True,
)

