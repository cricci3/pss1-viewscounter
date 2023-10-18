from setuptools import setup, find_packages
setup(name='prova',
      version='0.1.0',
      description='Some Python package',
      author='Me',
      author_email='me@example.com',
      license='MIT',
      packages=["application", "database"],
      package_dir={
            "": ".",
            "application": "./application",
            "database": "./database",
      },
      zip_safe=False)