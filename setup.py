from setuptools import setup, find_packages

setup(
   name='COMP9447',
   version='1.0',
   description='A set-up file for github actions to run for automated least priviledge enforcement',
   author='Zachary Ngooi',
   packages=['astStaticAnalysis', 'AWSPlayground', 'tests', 'frontend'],  #Defines user modules to be installed
)

