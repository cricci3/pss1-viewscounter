from setuptools import setup, find_packages

with open("README.md", "r") as f:
      long_description = f.read()

author_emails = [
    'damianoficara@gmail.com',
    # Aggiungi altre email se necessario
]

setup(name='2023_assignemt1_viewscounter',
      version='0.0.1',
      description='This assignment focuses on creating an application that counts and monitors user views',
      author='Team CED',
      author_email=author_emails,
      long_description=long_description,
      license='MIT',
      packages=["application", "database"],
      package_dir={
            "": ".",
            "application": "./application",
            "database": "./database",
      },
      zip_safe=False)