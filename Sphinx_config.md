csklearn

# Sphinx

Installation:

```
pip3 install Sphinx
```

[Here](https://developer.ridgerun.com/wiki/index.php/How_to_generate_sphinx_documentation_for_python_code_running_in_an_embedded_system)
is the reference of this documentation.

## Creating the documentation directory

Add the directory for documentation and the initial files:

```
mkdir docs
cd docs
sphinx-quickstart
```

Example Settings:

- Separate source and build directories (y/n) [n]: n
- Project name: udl-doc
- Author name(s): Daniel Runeda
- Project release []: 0.0.1
- Project language [en]: es

### Editing `conf.py`

- Add project path in `docs/config.py`:

You need to include the necessary source files folders in the PATH to be able
to generate the documentation from.

```
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
```

- Use docstring style: [Google Style](https://google.github.io/styleguide/pyguide.html#381-docstrings):

```
extensions = [
    'sphinx.ext.autodoc', # Grabs documentation from inside modules
    'sphinx.ext.napoleon', # supports Google-Style docstrings
    'sphinx.ext.viewcode' #ReStructured Text sources with the generated docs
]
master_doc = "index"
```

### Edit index.rst

The main `index.rst` file can be modified to include your application modules automatically (watch out for identation).

- Add modules in `docs/index.rst`

```
Welcome to udl-doc's documentation!
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
```

## Generating documentation

Before starting to generate documentation, **you might want to commit what you
have done so far**, so that automatically generated files after this point are
not versioned. In the moment that you version a file, you will have to
maintain it manually.

- Generating .rst files. The .rst files are automatically generated using the sphinx-apidoc command:

```bash
sphinx-apidoc -f -o . ..
```

### Generating the HTML documentation

Inside `docs` folder:

```bash
make html
```

### Visualization in a explorer:

We can open the documentation with, for example, firefox:

```bash
firefox _build/html/index.html
```

## Change Sphinx Theme:

You can customize Sphix. The mosth used theme is `sphinx_rtd_theme`:

```bash
sudo pip3 install sphinx_rtd_theme
```

We have to modify it in `docs/conf.py`:

```python
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme' #'alabaster'
```

## Summary

Once we have prepared the doc initialization, we will have to do usually:

```bash
sphinx-apidoc -f -o . ..
make html
firefox _build/html/index.html
```

# Sphinx in GitHub

The following section describes how to put documentation created on GitHub.

The additional steps are:


1. Create the file `docs/.nojekyll`. This is a particular file needed by GitHub.
2. Add to `docs/Makefile` the following:

   ```bash
   # github
   github:
   	@make html
   	@cp -a _build/html/. ../docs
   ```

   This is because github will search docs and needs a copy of the files generated by Sphinx.
3. Run the following commands:

   ```bash
   make clean
   ```

   ```bash
   make github
   ```
4. Update the GitHub repository and push changes. After that, go to your GitHub page, go to **settings**, and modify **GitHub Pages**. You can select in **source** the branch where you did the changes and select **docs/** folder.