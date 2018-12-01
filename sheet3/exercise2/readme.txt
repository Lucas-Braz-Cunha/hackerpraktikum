List of dependencies: gcc
Requirements: System must be Unix based (because of some functions used in the wrapper)


HOW TO execute:

  1.Before calling make go to file ./sandbox/sandbox.c and change value of PATH_TO_BLACKLIST
    to the path to your blacklist file. This file should have a list of ABSOLUTE PATHs to the
    blacklisted files. Also, the PATH_TO_BLACKLIST should be a absolute path.

  2. Execute make with the makefile in this folder

  3. Execute this command in the shell while in the folder exercise2:
    export LD_PRELOAD=$PWD/sandbox/libpreload.so

  4. Execute the test program (or the program of your choice), it is located ./test_program/test

  Obs: unset LD_PRELOAD to remove the wrapper lib.


Answer to quesstion about "breaking the sandbox":


How can a malicious program break out of the sandbox?

1. Using static libraries during compilation:

--with-shared=no --with-static=yes

2. pre-script that changes the LD_PRELOAD variable.(?)

3. Write its own functions to execute the intented routine.(?)

// #define _GNU_SOURCE
