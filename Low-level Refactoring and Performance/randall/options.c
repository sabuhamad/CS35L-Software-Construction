#include <stddef.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <unistd.h>
#include "options.h"

struct op;
struct op process_options(int argc, char **argv) {
   /* Check arguments.  */
   // initialize struct
    struct op options;
    options.input = NULL;
    options.output = NULL;
    int i;
    
    //include additional args passed
    if (argc >= 2 && strtoll(argv[argc-1], NULL, 10) != NULL)
    {
        options.nbytes = strtoll(argv[argc-1], NULL, 10);
    }
    else
    {
        options.nbytes = -1;
    }
    
    // check all arguments and account for any existing ones
    while ((i = getopt(argc, argv, "i:o:")) != -1)
    {
        if (i == 'i')
        {
            options.input = optarg;
        }
        else if(i == 'o')
        {
            options.output = optarg;
        }
        else
        {
            fprintf(stderr, "Error: Incorrect Inputs \n");
            exit(1);
        }
    }
    
    return options;
}
