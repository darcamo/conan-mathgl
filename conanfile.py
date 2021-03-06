#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool
import shutil
import os
# import svn.remote


class MathglConan(ConanFile):
    name = "mathgl"
    version = "2.4.3"
    license = "LGPL-3.0-only | GPL-3.0-only"
    url = "https://github.com/joakimono/conan-mathgl"
    author = "Joakim Haugen (joakim.haugen@gmail.com)"
    homepage = "http://mathgl.sourceforge.net"
    description = "MathGL is a library for making high-quality scientific graphics under Linux and Windows."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {
        "lgpl": [True, False],
        "double_precision": [True, False],
        "rvalue_support": [True, False],
        "pthread": [True, False],
        "pthr_widget": [True, False],
        "openmp": [True, False],
        "opengl": [True, False],
        "glut": [True, False],
        "fltk": [True, False],
        "wxWidgets": [True, False],
        "qt5": [True, False],
        "zlib": [True, False],
        "png": [True, False],
        "jpeg": [True, False],
        "gif": [True, False],
        "pdf": [True, False],
        "gsl": [True, False],
        "hdf5": [True, False],
        "mpi": [True, False],
        "ltdl": [True, False],
        "all_swig": [True, False]
    }
    default_options = ("lgpl=False", "double_precision=True",
                       "rvalue_support=False", "pthread=False",
                       "pthr_widget=False", "openmp=True", "opengl=True",
                       "glut=False", "fltk=False", "wxWidgets=False",
                       "qt5=False", "zlib=True", "png=True", "jpeg=True",
                       "gif=False", "pdf=True", "gsl=False", "hdf5=False",
                       "mpi=False", "ltdl=False", "all_swig=False")
    cmake_options = {}

    def add_cmake_opt(self, val, doAdd):
        if doAdd:
            self.cmake_options["enable-{}".format(val)] = 'ON'
        else:
            self.cmake_options["enable-{}".format(val)] = 'OFF'

    def system_requirements(self):
        installer = SystemPackageTool()
        if (self.options.opengl or self.options.glut) and os_info.is_linux:
            if tools.os_info.linux_distro == "arch":
                installer.install("freeglut")
            else:
                installer.install("freeglut3-dev")  # Name in Ubuntu

        if self.options.openmp and os_info.is_linux:
            if tools.os_info.linux_distro == "arch":
                installer.install("openmp")
            else:
                installer.install("libomp-dev")  # Name in Ubuntu

        if self.options.qt5:
            if tools.os_info.linux_distro == "arch":
                installer.install("qt5-base")

        if self.options.wxWidgets:
            if tools.os_info.linux_distro == "arch":
                installer.install("wxgtk2")

        if self.options.fltk:
            if tools.os_info.linux_distro == "arch":
                installer.install("fltk")

    def requirements(self):

        self.add_cmake_opt("double", self.options.double_precision)
        self.add_cmake_opt("mpi", self.options.mpi)
        self.add_cmake_opt("opengl", self.options.opengl)
        self.add_cmake_opt("rvalue", self.options.rvalue_support)
        self.add_cmake_opt(
            "pthread", self.options.pthread
        )  # Either enable pthread of openmp but not both at the same time
        self.add_cmake_opt("openmp", self.options.openmp)
        self.add_cmake_opt("ltdl", self.options.ltdl)

        self.add_cmake_opt("lgpl", self.options.lgpl)
        self.add_cmake_opt("pthr-widget",
                           self.options.pthr_widget)  # pthread widget
        self.add_cmake_opt("glut", self.options.glut)
        self.add_cmake_opt("fltk", self.options.fltk)
        self.add_cmake_opt("wx", self.options.wxWidgets)
        self.add_cmake_opt("qt5", self.options.qt5)
        self.add_cmake_opt("zlib", self.options.zlib)
        self.add_cmake_opt("png", self.options.png)
        self.add_cmake_opt("jpeg", self.options.jpeg)
        self.add_cmake_opt("gif", self.options.gif)
        self.add_cmake_opt("pdf", self.options.pdf)
        self.add_cmake_opt("mpi", self.options.mpi)
        self.add_cmake_opt("ltdl", self.options.ltdl)
        if not self.options.lgpl:
            self.add_cmake_opt("gsl", self.options.gsl)
            self.add_cmake_opt("hdf5", self.options.hdf5)
            self.add_cmake_opt("all-swig", self.options.all_swig)

        # expected to be found w/o conan: opengl, glut, fltk, wxwidgets, mpi, ltdl, gsl, qt
        if self.options.zlib:
            self.requires("zlib/[>=1.2.11]@conan/stable")
            # self.options["zlib"].shared = False
        if self.options.png:
            self.requires("libpng/[>=1.6.34]@bincrafters/stable")
            # self.options["libpng"].shared = False
        if self.options.jpeg:
            self.requires("libjpeg-turbo/[>=1.5.2]@bincrafters/stable")
            # self.options["libjpeg-turbo"].shared = False
            # set jpeg version 62
        if self.options.gif:
            self.requires("giflib/[>=5.1.3]@bincrafters/stable")
            # self.options["giflib"].shared = False
        if self.options.pdf:
            self.requires("libharu/2.3.0@darcamo/stable")
            # self.options["libharu"].shared = False
        if self.options.hdf5:
            if not self.options.lgpl:
                self.requires("hdf5/[>=1.10.5]")
                # self.options["HDF5"].shared = False

    def source(self):
        tools.get(
            "http://downloads.sourceforge.net/mathgl/mathgl-2.4.2.1.tar.gz")
        shutil.move("mathgl-2.4.2.1/", "sources")

        tools.replace_in_file(
            "sources/CMakeLists.txt", "project( MathGL2 )",
            '''project( MathGL2 )
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

        tools.replace_in_file(
            "sources/CMakeLists.txt",
            "set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${MathGL2_SOURCE_DIR}/scripts)",
            '''set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${MathGL2_SOURCE_DIR}/scripts)'''
        )

        tools.replace_in_file(
            "sources/CMakeLists.txt", '''	find_library(HPDF_LIB hpdf)
	if(NOT HPDF_LIB)
		message(SEND_ERROR "Couldn't find libHaru or libhpdf.")
	endif(NOT HPDF_LIB)
	find_path(HPDF_INCLUDE_DIR hpdf_u3d.h)
	if(NOT HPDF_INCLUDE_DIR)
		message(SEND_ERROR "Couldn't find headers of 3d-enabled version of libhpdf.")
	endif(NOT HPDF_INCLUDE_DIR)''', '''    find_package(Libharu REQUIRED)
    include_directories(${LIBHARU_INCLUDE_DIR})
    set(MGL_DEP_LIBS ${LIBHARU_LIBRARIES} ${MGL_DEP_LIBS})''')

    def build(self):
        cmake = CMake(self)
        os.mkdir("build")
        shutil.move("conanbuildinfo.cmake", "build/")
        cmake.definitions.update(self.cmake_options)
        if self.settings.os == "Windows":
            cmake.definitions["enable-dep-dll"] = "ON"
        cmake.configure(source_folder="sources", build_folder="build")
        cmake.build()
        cmake.install()

    def package_info(self):

        self.cpp_info.libs = ["mgl"]
        if self.options.fltk:
            self.cpp_info.libs.append('mgl-fltk')
        if self.options.glut:
            self.cpp_info.libs.append('mgl-glut')
        if self.options.qt5:
            self.cpp_info.libs.append('mgl-qt5')
            self.cpp_info.libs.append('mgl-qt')
            if self.options.fltk:
                self.cpp_info.libs.append('mgl-wnd')
        if self.options.wxWidgets:
            self.cpp_info.libs.append('mgl-wx')

        self.cpp_info.libs.append("dl")

        # if not self.options.shared and self.settings.compiler == "Visual Studio":
        #     for lib in range(len(self.cpp_info.libs)):
        #         self.cpp_info.libs[lib] += "-static"
        # if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
        #     for lib in range(len(self.cpp_info.libs)):
        #         self.cpp_info.libs[lib] += "d"
