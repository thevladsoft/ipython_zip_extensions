ipython_zip_extensions
======================
        
Standard %install_ext magic in IPython claims that it can install extensions that are either .py or .zip. However do not
expect a .zip extension to work out-of-the-box: you will need to do some hand-waiving as well as sys.path manipulations.
        
ipython_zip_extensions solves this problem by allowing you to install .zip, .tar.gz and .tgz extensions from local and
remote hosts.

Usage
-----
        
1. Install: `%install_ext https://raw.github.com/mksenzov/ipython_zip_extensions/master/zip_extensions.py`
2. Load: `%load_ext zip_extensions`
3. Now you can manage your zip extensions:

    * Install: %install_zip_ext /Users/foo/bar.zip
    * Load: %load_zip_ext extension_name
    * Unload: %unload_zip_ext extension_name
    * Reload: %reload_zip_ext extension_name
        
[Optionally] you can replace the standard ipython magics by calling `%transparent_zip_extensions_magic` after you have 
loaded zip_extensions. In this case zip_extensions will replace standard magic functions:
        
    * %install_ext
    * %load_ext
    * %unload_ext
    * %reload_ext
        
After replacing standard magics .zip, .tar.gz and .tgz will be managed by ipython_zip_extensions, while standard
implementation will take care of .py extensions.

Troubleshooting
---------------

If you have problems with ipython_zip_extensions you can enabled debug logging with `%debug_zip_extensions on`. To
disable logging use `%debug_zip_extensions off`.
