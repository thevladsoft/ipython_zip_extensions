import urllib2
import urlparse
from IPython import get_ipython
from IPython.core.magic import (Magics, magics_class, line_magic)
from IPython.core.magics.extension import ExtensionMagics
import os
import sys
import zipfile
import tarfile
import logging


@magics_class
class ZipExtensionsMagics(Magics):
    def __init__(self, shell):
        super(ZipExtensionsMagics, self).__init__(shell)

        self.logger = logging.getLogger(__name__)
        self.logger.handlers = []
        self.logger.addHandler(logging.StreamHandler())

        self.ipython = shell
        self.extension_magics = ExtensionMagics(self.ipython)
        self.extensions_dir = os.path.join(self.ipython.ipython_dir, 'extensions')
        self.__update_sys_path()


    @line_magic
    def install_zip_ext(self, line):
        name = self.__url2name(line)
        self.logger.debug("name: %s" % name)

        if name.endswith(".zip") or name.endswith(".gz") or name.endswith(".tgz"):
            if not os.path.exists(line):
                local_path = self.__download(line)
            else:
                local_path = self.__copy(line)

            base_name = os.path.basename(local_path)
            zip_file = os.path.join(self.extensions_dir, base_name)

            if base_name.endswith(".zip"):
                self.logger.info("zip file: %s" % zip_file)
                z = zipfile.ZipFile(zip_file)
                z.extractall(self.extensions_dir)
            else:
                self.logger.info("tar file: %s" % zip_file)
                tar = tarfile.open(zip_file)
                tar.extractall(self.extensions_dir)

            self.logger.debug("cleanup file: %s" % zip_file)
            os.remove(os.path.join(self.extensions_dir, zip_file))

            self.__update_sys_path()
            return

        self.extension_magics.install_ext(line)

    def __update_sys_path(self):
        self.logger.debug("update sys path")
        index = set(sys.path)
        for root, dirs, files in os.walk(self.extensions_dir):
            for d in dirs:
                rel_path = os.path.relpath(os.path.join(root, d), self.extensions_dir)

                hidden = False
                for element in rel_path.split(os.sep):
                    if element.startswith("."):
                        hidden = True

                if not hidden:
                    path = os.path.join(self.extensions_dir, root, d)

                    if path not in index:
                        self.logger.debug("add path: %s" % path)
                        sys.path.append(path)
                        index.add(path)


    def __url2name(self, url):
        return os.path.basename(urlparse.urlsplit(url)[2])

    def __download(self, url):
        self.logger.debug("__download: %s" % url)
        localName = self.__url2name(url)
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)

        if 'Content-Disposition' in res.info():
            # If the response has Content-Disposition, we take file name from it
            localName = res.info()['Content-Disposition'].split('filename=')[1]
            if localName[0] == '"' or localName[0] == "'":
                localName = localName[1:-1]
        elif res.url != url:
            # if we were redirected, the real file name we take from the final URL
            localName = self.__url2name(res.url)

        local_path = self.__serialize(res, localName)

        self.logger.debug("downloaded to: %s" % local_path)
        return local_path

    def __copy(self, file_path):
        f = open(file_path, 'rb')
        local_name = os.path.basename(file_path)
        try:
            local_path = self.__serialize(f, local_name)
            self.logger.debug("copied to: %s" % local_path)
            return local_path
        finally:
            f.close()

    def __serialize(self, stream, local_name):
        """
        Serialize generic stream into IPython extensions dir.
        """
        local_path = os.path.join(self.extensions_dir, local_name)
        f = open(local_path, 'wb')
        f.write(stream.read())
        f.close()
        return local_path

    @line_magic
    def load_zip_ext(self, line):
        self.logger.debug("%%load_ext(%s)" % line)
        self.extension_magics.load_ext(line)

    @line_magic
    def unload_zip_ext(self, line):
        self.logger.debug("%%unload_ext(%s)" % line)
        self.extension_magics.unload_ext(line)

    @line_magic
    def reload_zip_ext(self, line):
        self.unload_zip_ext(line)
        self.load_zip_ext(line)

    @line_magic
    def debug_zip_extensions(self, line):
        if line == "on":
            self.logger.setLevel(logging.DEBUG)
        elif line == "off":
            self.logger.setLevel(logging.FATAL)
        else:
            print "Unsupported value, should be [on|off]"


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
