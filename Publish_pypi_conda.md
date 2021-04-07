## Checklist to upload the module on Pypi and Conda
### Pypi
Modify the code and then:
1. update the `README.md` file and in particular the change log.

2. Commit everything with `git`.

3. use `git tag` to define a new release. The message should be a summary of the change log. For instance:

   ```
   git tag -a 0.1 -m "working python module, only able to accept `vcf` files"
   ```

4. convert the `README.md` to `.rst` with pandoc (pypi wants a `rst` file!):

    ```
    pandoc -f markdown -t rst README.md -o README.rst
    ```

5. build the python module:
    ```
    python setup.py sdist
    ```

6. upload it:
    ```
    twine upload dist/<file.tar.gz>
    ```

### Conda

First I run conda skeleton:

```
cd build_conda_package
conda skeleton pypi fast-lineage-caller
```

I change some fields on the `yaml` file (path of the file on pypi, github ID: you can get it [here](https://api.github.com/users/ejfresch).

Then I can directly build the package, since this is a pure python package:

```
conda-build fast-lineage-caller
```

I am ready to upload the linux-64 package:

```
anaconda upload /home/lf61/sw/miniconda3/conda-bld/linux-64/fast-lineage-caller-0.1-py36_0.tar.bz2
```

I can generate the packages for the other platforms:

```
conda convert --platform all /home/lf61/sw/miniconda3/conda-bld/linux-64/fast-lineage-caller-0.1-py36_0.tar.bz2 -o output
```

And upload them:

```
for i in `find output -name "*.tar.bz2"`;do anaconda upload ${i};done
```

If you need to provide the package for different python versions rebuild the package:

```
conda-build --python 3.7 fast-lineage-caller
```



