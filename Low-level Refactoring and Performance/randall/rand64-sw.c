#include <stdio.h>
#include <stdlib.h>
#include "rand64-sw.h"

/* Input stream containing random bytes.  */
FILE *urandstream;
char* file_input;
/* Initialize the software rand64 implementation.  */
void
software_rand64_init (void)
{
  extern char* file;  // Declare 'file' from randall.c as an external variable.
  file_input = file;  // Assign the value of 'file' to 'file_input'.
  urandstream = fopen (file_input, "r");
  if (!urandstream)
  {
    urandstream = fopen (file_input + 1, "r");
  }
  if(!urandstream)
    abort ();
}

/* Return a random value, using software operations.  */
unsigned long long
software_rand64 (void)
{
  unsigned long long int x;
  if (fread (&x, sizeof x, 1, urandstream) != 1)
    abort ();
  return x;
}

/* Finalize the software rand64 implementation.  */
void
software_rand64_fini (void)
{
  fclose (urandstream);
}
