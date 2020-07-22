## Checklist to upload the module on Pypi and Conda
### Pypi
Modify the code and then:
1. Commit everything with `git`.

2. update the `README.md` file and in particular the change log.

3. use `git tag` to define a new release. The message should be a summary of the change log. For instance:

   ```
   git tag -a 0.2.1 -m "bin/metatools_convert was not included in setup.py (bugfix)"
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