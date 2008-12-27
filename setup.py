#!/usr/bin/python -u
#
# Python Bindings for LZMA
#
# Copyright (c) 2004-2008 by Joachim Bauch, mail@joachim-bauch.de
# 7-Zip Copyright (C) 1999-2005 Igor Pavlov
# LZMA SDK Copyright (C) 1999-2005 Igor Pavlov
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# $Id$
#
import sys, os
from warnings import warn

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, Extension

class UnsupportedPlatformWarning(Warning):
    pass

# set this to any true value to enable multithreaded compression
ENABLE_MULTITHREADING = True

# set this to any true value to add the compatibility decoder
# from version 0.0.3 to be able to decompress strings without
# the end of stream mark and you don't know their lengths
ENABLE_COMPATIBILITY = True

# compile including debug symbols on Windows?
COMPILE_DEBUG = False

# are we running on Windows?
IS_WINDOWS = sys.platform in ('win32', )

libraries = []
if IS_WINDOWS:
    libraries += ['user32', 'oleaut32']

include_dirs = [
".",
]

if sys.platform == 'darwin':
    # additional include directories are required when compiling on Darwin platforms
    include_dirs += [
        "/var/include",
    ]

library_dirs = [
".",
]

mt_platforms = (
    'win32',
)

if ENABLE_MULTITHREADING and not sys.platform in mt_platforms:
    warn("""\
Multithreading is not supported on the platform "%s",
please contact mail@joachim-bauch.de for more informations.""" % (sys.platform), UnsupportedPlatformWarning)
    ENABLE_MULTITHREADING = 0    

descr = "Python bindings for the LZMA library by Igor Pavlov."
long_descr = """PyLZMA provides a platform independent way to read and write data
that has been compressed or can be decompressed by the LZMA library by Igor Pavlov."""
try: version = open('version.txt', 'rb').read().strip()
except: version = 'unknown'
modules = ['py7zlib']
c_files = ['pylzma.c', 'pylzma_decompressobj.c', 'pylzma_compressfile.cpp',
           'pylzma_decompress.c', 'pylzma_compress.cpp', 'pylzma_guids.cpp']
compile_args = []
link_args = []
macros = []
if IS_WINDOWS:
    macros.append(('WIN32', 1))
    if COMPILE_DEBUG:
        compile_args.append('/Zi')
        compile_args.append('/MTd')
        link_args.append('/DEBUG')
    else:
        compile_args.append('/MT')
if not IS_WINDOWS:
    # disable gcc warning about virtual functions with non-virtual destructors
    compile_args.append(('-Wno-non-virtual-dtor'))
if ENABLE_MULTITHREADING:
    macros.append(('COMPRESS_MF_MT', 1))
lzma_files = ('src/LzmaStateDecode.c', 'src/CPP/7zip/Compress/LZMA/LZMAEncoder.cpp',
    'src/CPP/7zip/Compress/RangeCoder/RangeCoderBit.cpp', 'src/CPP/Common/CRC.cpp',
    'src/CPP/7zip/Compress/LZ/LZInWindow.cpp', 'src/CPP/7zip/Common/StreamUtils.cpp',
    'src/CPP/7zip/Common/OutBuffer.cpp', 'src/CPP/Common/Alloc.cpp', 'src/CPP/Common/NewHandler.cpp', )
if ENABLE_MULTITHREADING:
    lzma_files += ('src/CPP/7zip/Compress/LZ/MT/MT.cpp', 'src/CPP/OS/Synchronization.cpp', )
if ENABLE_COMPATIBILITY:
    c_files += ('pylzma_decompress_compat.c', 'pylzma_decompressobj_compat.c', )
    lzma_files += ('src/LzmaCompatDecode.c', )
    macros.append(('WITH_COMPAT', 1))

c_files += [os.path.normpath(os.path.join('.', x)) for x in lzma_files]
extens = [
    Extension('pylzma', c_files, include_dirs=include_dirs, libraries=libraries,
              library_dirs=library_dirs, define_macros=macros, extra_compile_args=compile_args,
              extra_link_args=link_args),
]

if IS_WINDOWS:
    operating_system = 'Microsoft :: Windows'
else:
    operating_system = 'POSIX :: Linux'

setup(
    name = "pylzma",
    version = version,
    description = descr,
    author = "Joachim Bauch",
    author_email = "mail@joachim-bauch.de",
    url = "http://www.joachim-bauch.de/projects/python/pylzma/",
    license = 'LGPL',
    keywords = "lzma compression",
    long_description = long_descr,
    platforms = sys.platform,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: %s' % operating_system,
    ],
    py_modules = modules,
    ext_modules = extens,
    test_suite = 'tests',
    zip_safe = False,
)
