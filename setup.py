from setuptools import setup, find_packages

setup(
   name='COMP9447',
   version='1.0',
   description='A useful module',
   author='Man Foo',
   author_email='foomail@foo.example',
   packages=['StaticAnalysisBoto3', 'astStaticAnalysis', 'AWSPlayground', 'tests'],  #Define user modules to be installed
)