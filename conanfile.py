import os
from distutils.spawn import find_executable
from conans import ConanFile, ConfigureEnvironment
from conans.tools import cpu_count, vcvars_command, os_info, SystemPackageTool, download, untargz
from multiprocessing import cpu_count

class QtBaseConan(ConanFile):
    """ Qt Base Conan package """

    name = "QtSvg"
    version = "5.7.1"
    majorVersion = "5.7"
    requires = "QtBase/5.7.1@russelltg/stable"
    settings = "os", "arch", "compiler", "build_type"
    url = "http://github.com/kde-frameworks-conan/{}".format(name.lower())
    license = "http://doc.qt.io/qt-5/lgpl.html"
    generators = "qmake"
    short_paths = True

    
    
    folderName = "{}-opensource-src-{}".format(name.lower(), version)

    def source(self):
        zipName = "{}.tar.gz".format(self.folderName)
        zipUrl = "http://download.qt.io/official_releases/qt/{}/{}/submodules/{}".format(self.majorVersion, self.version, zipName)
        download(zipUrl, zipName)
        untargz(zipName)
        os.unlink(zipName)
        

    def build(self):
        self.output.info("Configuring to {}".format(self.conanfile_directory))
        with open(os.path.join(self.conanfile_directory, self.folderName, "qtsvg.pro"), "w") as QMakeFile:
            QMakeFile.write("CONFIG += conan_basic_setup\n"
                            "include(../conanbuildinfo.pri)\n"
                            "load(qt_parts)\n")
        self.run("cd {} && qmake .".format(os.path.join(self.conanfile_directory, self.folderName)))
        self.run("cd {} && make -j{}".format(os.path.join(self.conanfile_directory, self.folderName), cpu_count()))
        
    def package(self):
        self.copy("*", dst="include", src=os.path.join(self.folderName, "include"))
        self.copy("*", dst="lib", src=os.path.join(self.folderName, "lib"))
