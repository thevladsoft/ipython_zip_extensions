from IPython import get_ipython
from IPython.core.magic import (Magics, magics_class, line_magic)
from IPython.core.magics.extension import ExtensionMagics
import os, sys
import zipfile


@magics_class
class ZipExtensionsMagics(Magics):
    def __init__(self, shell):
        super(ZipExtensionsMagics, self).__init__(shell)
        self.ipython = shell
        self.extension_magics = ExtensionMagics(self.ipython)
        self.extension_dir = os.path.join(self.ipython.ipython_dir, 'extensions')

    @line_magic
    def install_zip_ext(self, line):
        self.extension_magics.install_ext(line)

        if line.endswith(".zip"):
            f = open(line, 'rb')

            try:
                z = zipfile.ZipFile(f)

                for name in z.namelist():
                    z.extract(name, self.extension_dir)
                    path = os.path.join(self.extension_dir, name)
                    #  If we extracted a folder make sure that the data is available
                    if os.path.isdir(path):
                        sys.path += [os.path.join(self.extension_dir, name)]
            finally:
                f.close()

            zip_file = os.path.join(self.extension_dir, os.path.basename(line))
            print "remove zip: %s" % zip_file
            os.remove(os.path.join(self.extension_dir, zip_file))


    @line_magic
    def load_zip_ext(self, line):
        path = os.path.join(self.extension_dir, line)
        if os.path.isdir(path):
            self.extension_magics.load_ext("%s.%s" % (line, os.path.basename(line)))
        else:
            self.extension_magics.load_ext(line)


    @line_magic
    def unload_zip_ext(self, line):
        path = os.path.join(self.extension_dir, line)
        if os.path.isdir(path):
            self.extension_magics.unload_ext("%s.%s" % (line, os.path.basename(line)))
        else:
            self.extension_magics.unload_ext(line)


    @line_magic
    def reload_zip_ext(self, line):
        self.unload_zip_ext(line)
        self.load_zip_ext(line)


@magics_class
class TransparentZipExtensionsMagics(Magics):
    def __init__(self, shell):
        super(TransparentZipExtensionsMagics, self).__init__(shell)
        self.zip_ext_magics = ZipExtensionsMagics(shell)

    @line_magic
    def install_ext(self, line):
        self.zip_ext_magics.install_zip_ext(line)

    @line_magic
    def load_ext(self, line):
        self.zip_ext_magics.load_zip_ext(line)

    @line_magic
    def unload_ext(self, line):
        self.zip_ext_magics.unload_zip_ext(line)

    @line_magic
    def reload_ext(self, line):
        self.zip_ext_magics.reload_zip_ext(line)


def transparent_zip_extensions_magic(line):
    get_ipython().register_magics(TransparentZipExtensionsMagics)


def load_ipython_extension(ipython):
    ipython.register_magics(ZipExtensionsMagics)
    ipython.register_magic_function(transparent_zip_extensions_magic, 'line')
