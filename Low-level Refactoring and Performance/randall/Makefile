# Make x86-64 random byte generators.

# Copyright 2015, 2020, 2021 Paul Eggert

# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

# Optimization level.  Change this -O2 to -Og or -O0 or whatever.
OPTIMIZE =

# The C compiler and its options.
CC = gcc
CFLAGS = $(OPTIMIZE) -g3 -Wall -Wextra -fanalyzer \
  -march=native -mtune=native -mrdrnd

# The archiver command, its options and filename extension.
TAR = tar
TARFLAGS = --gzip --transform 's,^,randall/,'
TAREXT = tgz

default: randall

randall: randall.c rand64-hw.o rand64-sw.o output.o options.o mrand48.o
	$(CC) $(CFLAGS) $^ -o $@

rand64-hw.o: rand64-hw.c
	$(CC) $(CFLAGS) -c rand64-hw.c

rand64-sw.o: rand64-sw.c
	$(CC) $(CFLAGS) -c rand64-sw.c

options.o: options.c
	$(CC) $(CFLAGS) -c options.c

output.o: output.c 
	$(CC) $(CFLAGS) -c output.c

mrand48.o: mrand48.c
	$(CC) $(CFLAGS) -c mrand48.c

assignment: randall-assignment.$(TAREXT)
assignment-files = COPYING Makefile randall.c
randall-assignment.$(TAREXT): $(assignment-files)
	$(TAR) $(TARFLAGS) -cf $@ $(assignment-files)

submission-tarball: randall-submission.$(TAREXT)
submission-files = $(assignment-files)\
notes.txt options.c options.h mrand48.h mrand48.c rand64-sw.c \
rand64-sw.h rand64-hw.c rand64-hw.h output.c output.h 
randall-submission.$(TAREXT): $(submission-files)
	$(TAR) $(TARFLAGS) -cf $@ $(submission-files)

repository-tarball:
	$(TAR) -czf randall-git.tgz .git

.PHONY: default clean assignment submission-tarball repository-tarball

clean:
	rm -f *.o *.$(TAREXT) randall

check:
	@echo "Testing randall program..."
	@echo "Generating 10 bytes of random data..."
	@./randall 10 > output.txt
	@echo "Checking output length..."
	@if [ `wc -c < output.txt` -eq 10 ]; then \
    	echo "Test passed!"; \
	else \
	    echo "Test failed!"; \
	fi
	@rm output.txt
	@echo "Generating 100 bytes of random data..."
	@./randall 100 > output.txt
	@echo "Checking output length..."
	@if [ `wc -c < output.txt` -eq 100 ]; then \
    	echo "Test passed!"; \
	else \
	    echo "Test failed!"; \
	fi
	@rm output.txt
	@echo "Generating 10 bytes of random data with option -i rdrand..."
	@./randall -i rdrand 10 > output.txt
	@echo "Checking output length..."
	@if [ `wc -c < output.txt` -eq 10 ]; then \
    	echo "Test passed!"; \
	else \
	    echo "Test failed!"; \
	fi
	@rm output.txt
	@echo "Generating 10 bytes of random data with option -i mrand48_r..."
	@./randall -i mrand48_r 10 > output.txt
	@echo "Checking output length..."
	@if [ `wc -c < output.txt` -eq 10 ]; then \
    	echo "Test passed!"; \
	else \
	    echo "Test failed!"; \
	fi
	@rm output.txt
	@echo "Generating 2 bytes of random data with option -i /input.txt..."
	@touch input.txt 
	@echo '23333' >> input.txt 
	@echo '122' >> input.txt
	@echo '133' >> input.txt
	@echo '144' >> input.txt
	@echo '155' >> input.txt
	@echo '166' >> input.txt
	@./randall -i /input.txt 2 > output.txt
	@echo "Checking output length..."
	@if [ `wc -c < output.txt` -eq 2 ]; then \
    	echo "Test passed!"; \
	else \
	    echo "Test failed!"; \
	fi
	@rm input.txt
	@rm output.txt
	@echo "Generating 10 bytes of random data with option -i /dev/urandom ..."
	@./randall -i /dev/urandom 10 > output.txt
	@echo "Checking output length..."
	@if [ `wc -c < output.txt` -eq 10 ]; then \
    	echo "Test passed!"; \
	else \
	    echo "Test failed!"; \
	fi
	@rm output.txt
	@echo "Generating 10 bytes of random data with option -o stdio..."
	@./randall -o stdio 10 > output.txt
	@echo "Checking output length..."
	@if [ `wc -c < output.txt` -eq 10 ]; then \
    	echo "Test passed!"; \
	else \
	    echo "Test failed!"; \
	fi
	@rm output.txt
	@echo "Generating 10 bytes of random data with option -o 100..."
	@./randall -o 100 10 > output.txt
	@echo "Checking output length..."
	@if [ `wc -c < output.txt` -eq 10 ]; then \
    	echo "Test passed!"; \
	else \
	    echo "Test failed!"; \
	fi
	@rm output.txt
	@echo "Generating 10 bytes of random data with option -o 2..."
	@./randall -o 2 10 > output.txt
	@echo "Checking output length..."
	@if [ `wc -c < output.txt` -eq 10 ]; then \
    	echo "Test passed!"; \
	else \
	    echo "Test failed!"; \
	fi
	@rm output.txt
	@echo "Generating 10 bytes of random data with option -o 2 -i rdrand..."
	@./randall -o 2 -i rdrand 10 > output.txt
	@echo "Checking output length..."
	@if [ `wc -c < output.txt` -eq 10 ]; then \
    	echo "Test passed!"; \
	else \
	    echo "Test failed!"; \
	fi
	@rm output.txt
	@echo "Generating 10 bytes of random data with option -o 2 -i mrand48_r..."
	@./randall -o 2 -i mrand48_r 10 > output.txt
	@echo "Checking output length..."
	@if [ `wc -c < output.txt` -eq 10 ]; then \
    	echo "Test passed!"; \
	else \
	    echo "Test failed!"; \
	fi
	@rm output.txt
	@echo "Generating 4 bytes of random data with option -o 2 -i /input.txt..."
	@touch input.txt 
	@echo '23333' >> input.txt 
	@echo '122' >> input.txt
	@echo '133' >> input.txt
	@echo '144' >> input.txt
	@echo '155' >> input.txt
	@echo '166' >> input.txt
	@./randall -o 2 -i /input.txt 4 > output.txt
	@echo "Checking output length..."
	@if [ `wc -c < output.txt` -eq 4 ]; then \
    	echo "Test passed!"; \
	else \
	    echo "Test failed!"; \
	fi
	@rm input.txt
	@rm output.txt