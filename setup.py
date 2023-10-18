from setuptools import setup, find_packages

setup(
    name='prova',
    version='0.1.0',
    description='Some Python package',
    author='Me',
    author_email='me@example.com',
    license='MIT',
    packages=find_packages(),  # Utilizza find_packages() per trovare automaticamente i pacchetti
    zip_safe=False
)
