
# Instructions to install the CGNS library

The code in this project depends on the CGNS lib, however, it only works for C
or Fortran code. To make it work also in Python, we need to create a Fortran
file and implement all basic operations in there and, then, convert this Fortran
file into a module that will be imported by the Python. This convertion makes
use of `f2py`.


## Dependencies:

- Download the CGNS library *version 3.3.0* (Google it to find the link)
- Install `f2py` (I think now it comes with Numpy)


## Installing CGNS from source:

Unpack the downloaded lib in a folder outside of this project. Enter its src/ 
subdirectory inside the unzipped root folder and type in your terminal: 
`$ ./configure --help`

A series of installation options will appear to you. Deppending on the
application, it may be useful to have a shared library that can be used by
another code (for example, post-process codes written in Python that uses
Fortran routines wrapped with *f2py*). The shared library extension ends with
"*.so*". But also, sometimes we want a static library (extension "*.a*") to be 
used to compile the fortran code and run it in some remote machine.

By default, a static CGNS library will be created. To create the dynamic lib,
one needs to use the flag "--enable-shared=all" during the compilation process.
Also, we need to choose the directory where the CGNS library will be installed.
This is done by using the flag  `--prefix=full_path_to_directory`, where
*full_path_to_directory* must be substituted with your desired path.

So that, we are left with:
```
$ ./configure --enable-shared=all --prefix=full_path_to_directory
```

Remember to indicate the full path to avoid any possible errors. 

As default, the CGNS library will be compiled using gfortran as compiler. To
alter that behavior, one needs to specify the compiler. For Intel compilers,
we have:
```
$ CC=icc FC=ifort ./configure --enable-shared=all --prefix=full_path_to_directory
```

After that, the *configure* executable will generate a Makefile.
The more recent versions of the CGNS library has a bug in this Makefile though.

At line 12 of the Makefile you have: `FOPTS   = $(FFLAGS) -I.`
Add at the end of this line the flag -fPIC, that is: `FOPTS   = $(FFLAGS) -I. -fPIC`


Save the Makefile and execute it. To execute with multiple threads, you can use
the -j flag. For instance, using 4 parallel processes, we have: `$ make -j4`

Then, type the following to install (sudo may be necessary in case of
authorization problems): `$ make install`


**Important detail:** when using shared libraries (\*.so), you need to indicate
its path in the system variable $LD_LIBRARY_PATH. Hence, add the following line
to your bash script e restart the terminal:
```
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:full_path_to_directory
```

After installing, go to your chosen `full_path_to_directory` and hit:
```
cp ./lib/libcgns.so .
```

**Troubleshooting:**

Some problems that may happen (although unlikely to happen) are:

* Sometimes "CC" and "CF" specifications from "configure" does not work.
If you think that this may be the problem, then you will have to fix this manually.
That is, open the configure file and specify manually who will be "CC" and "CF",
indicating the full path to the compiler that you want.

* Sometimes there may be conflicts between the compiler that the system used
to compile the CGNS library and the compiler it is using to run your fortran code.
This issue may occurs when you have different GCC libraries installed in your machine.
You can check which compiler is being applied using the "which" command in your
terminal. Try to compile the code indicating explicitly the compiler as it
pops up from "which" command, like: `/usr/local/bin/gfortran your_script`


## Creating our "custom" CGNS lib to use it in Python

Once the CGNS lib is installed, open the makefile (the one that sits next to
this README file) and inform the proper `full_path_to_directory` where the
CGNS lib was installed. Then, hit `make` to compile the library.

Check if the installation is correct with the command `ldd CGNS.cpython-38-x86_64-linux-gnu.so`
You should see all libs point to some memory address. If you see some "not found",
this means that something went wrong (probably due to some linking issue).

If everything is OK, then move this lib to the parent directory:

```
mv CGNS.cpython-38-x86_64-linux-gnu.so ../CGNS.so
```

This is going to put the lib next to your Python source code, so that when you
do a `import CGNS` in Python, it will find the lib.

If you want to place this CGNS lib somewhere else, you can also do that.
However, in this case you need to inform this new location in the PYTHONPATH.
