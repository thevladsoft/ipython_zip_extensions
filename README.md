ipython_zip_extensions
======================
        
Standard %install_ext magic in IPython can install extensions that are either .py or .zip. However do not expect a .zip
extension to work out-of-the-box if it contains multiple python files: you will need to do a lot of hand-waiving.
        
ipython_zip_extensions solves this problem by first calling standard installation magic, and then setting up the
environment allowing .zip extension containers to function properly.

Usage
-----
        
1. Install: `%install_ext https://raw.github.com/mksenzov/ipython_zip_extensions/master/zip_extensions.py`
2. Load: `%load_ext zip_extensions`
3. Now you can manage your zip extensions:

    * Install: `%install_zip_ext /Users/foo/bar.zip`
    * Uninstall:` %uninstall_zip_ext /Users/foo/bar.zip`
    * Reload: `%reload_zip_ext /Users/foo/bar.zip`
        
Optionally you can replace the standard ipython magics by calling %transparent_zip_extensions_magic after you have
loaded zip_extensions. In this case:
        
    * %install_ext
    * %uninstall_ext
    * %reload_ext
        
will start either delegating to standard IPython's %install_ext/%uninstall_ext/%reload_ext magics if you deal with .py,
or will use the new logic for .zip extensions.
    
    
    
        
    
