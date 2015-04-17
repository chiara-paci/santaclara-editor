import santaclara_editor.languages

def autodiscover():
    """
    Auto-discover INSTALLED_APPS santaclara_languages.py modules and fail silently when
    not present. This forces an import on them to register any santaclara editor bits they
    may want.
    """

    import copy
    from django.conf import settings
    from importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        language_register_pre=copy.copy(santaclara_editor.languages.language_register)
        # Attempt to import the app's santaclara_languages module.
        try:
            import_module('%s.santaclara_languages' % app)
        except:
            # Decide whether to bubble up this error. If the app just
            # doesn't have a santaclara_languages module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'santaclara_languages'):
                santaclara_editor.languages.language_register=language_register_pre
                raise
