#Santa Clara Editor

Santa Clara Editor is a Django app with a bbcode-style interpreter and
a widget with syntax highlighting to editing.

##Quick start

1. Build package:
   ```
        $ cd santaclara-editor/
        $ python setup.py sdist
   ```

2. Install package:
    ```
        $ cd santaclara-editor/
        $ pip install --user dist/santaclara_editor-<version>.tar.gz
    ```

3. Add "santaclara_editor" to your INSTALLED_APPS setting like this:
    ```
        INSTALLED_APPS = (
            ...
            'santaclara_editor',
            ...
        )
    ```


##Documentation

- [Template Filters](docs/santa_clara_editor.md)
- [Santa Clara Language](docs/santaclara_languages.md)
- [Widget](docs/widget.md)
- [How To Extend Language](docs/extend_language.md)


