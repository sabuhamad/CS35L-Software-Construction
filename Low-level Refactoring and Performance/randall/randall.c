/* Generate N bytes of random output.  */

/* When generating output this program uses the x86-64 RDRAND
   instruction if available to generate random numbers, falling back
   on /dev/random and stdio otherwise.

   This program is not portable.  Compile it with gcc -mrdrnd for a
   x86-64 machine.

   Copyright 2015, 2017, 2020 Paul Eggert

   This program is free software: you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

#include <cpuid.h>
#include <errno.h>
#include <immintrin.h>
#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "rand64-hw.h"
#include "rand64-sw.h"
#include "options.h"
#include "output.h"
#include "mrand48.h"

char* file;
/* Main program, which outputs N bytes of random data.  */
int main (int argc, char **argv)
{
  struct op options = process_options(argc, argv);
  if(options.nbytes == -1)
  {
    fprintf(stderr, "Error: Missing NBYTES argument\n");
    exit(1);
  }
  if (options.nbytes == 0)
  {
    return 0;
  }

  /* Now that we know we have work to do, arrange to use the
     appropriate library.  */
  void (*initialize) (void);
  unsigned long long (*rand64) (void);
  void (*finalize) (void);
  /* rdrand option used for hardware random number generation */
  if (!options.input || strcmp(options.input, "rdrand") == 0)
  {
      if (rdrand_supported ())
        {
          initialize = hardware_rand64_init;
          rand64 = hardware_rand64;
          finalize = hardware_rand64_fini;
        }
      else
        {
            fprintf(stderr, "Error: rdrand not supported \n");
            exit(1);
        }
  }
  /* mrand48_r option used for mrand48_r generation of random number */
  else if (strcmp(options.input, "mrand48_r") == 0)
  {
      initialize = mrand48_r_init;
      rand64 = use_mrand48_r;
      finalize = mrand48_r_fini;
  }
  /* /F option to use the file /F as a source of random data */
  else if (options.input[0] == '/')
  {
      file = options.input;
      initialize = software_rand64_init;
      rand64 = software_rand64;
      finalize = software_rand64_fini;
  }
  else
  {
    fprintf(stderr, "Error:\n./randall -i INPUTTYPE NBYTES\n./randall -o OUTPUTTYPE NBYTES\n");
            exit(1);
  }

  initialize ();
  int output_errno;

  if (options.output != NULL && strcmp(options.output, "stdio") != 0)
      output_errno = writeoutput(rand64, atoi(options.output), options.nbytes, false);
  else
      output_errno = writeoutput(rand64, 0, options.nbytes, true);
  
  finalize ();
  return !!output_errno;
}