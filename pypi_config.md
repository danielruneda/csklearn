# PyPI repository

## Start custom module

- Create the module folder: `csklearn` in the root of the project. Create all classes and functions desired inside.
- Create an `__init__.py` file.
- Each folder in the module, also needs an `__init__.py` file.
- The tree should be something like:

  ```bash
  ├── csklearn
  │   ├── feature_selection
  │   ├── __init__.py
  │   ├── metrics
  │   ├── model_selection
  │   ├── plots
  │   ├── preprocessing
  │   ├── samples
  │   ├── transformers
  │   └── utils
  ```
- Add all module folders in `csklearn/__init__.py` file:

  ```python
  from .feature_selection import *
  from .metrics import *
  from .model_selection import *
  from .plots import *
  from .transformers import *
  from .utils import *
  ```


## Configure PyPI

### Local configuration

- Create a `setup.py` file in root folder of the project.

  ```python
  from setuptools import setup

  setup(
      # Needed to silence warnings (and to be a worthwhile package)
      name='csklearn',
      url='https://github.com/danielruneda/csklearn',
      author='Daniel Runeda',
      author_email='danielruneda@gmail.com',
      # Needed to actually package something
      packages=['csklearn'],
      # Needed for dependencies
      install_requires=[
          'numpy'
          ],
      # *strongly* suggested for sharing
      version='0.0.0',
      # The license can be anything you like
      # license='MIT',
      # description='An example of a python package from pre-existing code',
      # We will also need a readme eventually (there will be a warning)
      # long_description=open('README.txt').read(),
      python_requires='>=3.6',
      # The package can not run directly from zip file
      zip_safe=False
  )
  ```
- Check if pip works well and there are no errors:

  ```bash
  pip install .
  ```
- If all works fine, the you should find the `csklearn` module with:

  ```bash
  pip list
  ```
- Now, you have installed the module and you can try it.

### Upload to PyPI

- Once you have your module ready, you can upload to PyPI. First of all, you need an account there: [PyPI](https://pypi.org/). You will need:

  ```bash
  pip install twine
  ```
- Then, create the following:

  - Create a file `csklearn/licence.txt`.
  - Create a file `csklearn/setup.cfg`
- Compile the code (this will create a tar archive):

  ```bash
  python setup.py sdist
  ```

  This create a distribution of our module:

  ```bash
  ├── dist
  │   └── csklearn-0.0.0.tar.gz
  ```
- To upload use (**read the warnings!**):

  ```bash
  twine upload dist/*
  ```

  And write your credentials
- **IMPORTANT WARNING!!!** If you use a name for the module, **you won't be allowed to create another one even if you delete the project!** To make tests, you can use **test-pypi** in the same way:

  ```bash
  twine upload --repository-url https://test.pypi.org/legacy/ dist/*
  ```

  In your test-pypi account you can see how to download with pip:

  ```bash
  pip install -i https://test.pypi.org/simple/ csklearn
  ```