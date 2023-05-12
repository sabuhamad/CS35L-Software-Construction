#ifndef OPTIONS_H
#define OPTIONS_H

struct op
{ int nbytes; char* input; char* output;};
struct op process_options(int argc, char **argv);

#endif
